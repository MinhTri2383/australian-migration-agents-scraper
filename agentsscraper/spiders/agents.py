import scrapy

from agentsscraper.items import AgentItem


class AgentsSpider(scrapy.Spider):
    name = "agents"
    allowed_domains = ["portal.mara.gov.au"]

    search_url = (
        "https://portal.mara.gov.au/"
        "search-the-register-of-migration-agents/"
    )
    base_url = "https://portal.mara.gov.au"

    async def start(self):
        yield scrapy.Request(
            self.search_url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_goto_kwargs": {
                    "wait_until": "domcontentloaded",
                    "timeout": 60_000,
                },
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        try:
            given_name = page.get_by_role(
                "textbox",
                name="Agent's given name",
            )
            await given_name.fill(" ")

            # Commented out the following line to scrape all agents.
            await page.get_by_role("checkbox", name="Non-commercial organisations").check()


            await page.get_by_role("button", name="Search").click()
            await page.get_by_role("table").wait_for(state="visible")

            while True:
                current_response = response.replace(
                    body=(await page.content()).encode("utf-8")
                )

                for agent in current_response.css("tbody tr"):
                    relative_url = agent.css(
                        "a.details-link.has-tooltip::attr(href)"
                    ).get()

                    if not relative_url:
                        continue

                    first_name = agent.css(
                        "td:nth-child(2)::text"
                    ).get()
                    last_name = agent.css(
                        "td:nth-child(1) a::text"
                    ).get()

                    yield response.follow(
                        url=relative_url,
                        callback=self.parse_agent_page,
                        meta={
                            "first_name": first_name,
                            "last_name": last_name,
                        },
                    )

                next_link = page.locator("a.entity-pager-next-link")
                parent_li = next_link.locator("xpath=..")

                aria_disabled = await next_link.get_attribute(
                    "aria-disabled"
                )
                parent_class = await parent_li.get_attribute("class") or ""

                if aria_disabled == "true" or "disabled" in parent_class.split():
                    self.logger.info("Reached the last page.")
                    break

                rows = page.locator("tbody tr")
                first_row_before = (await rows.first.inner_text()).strip()

                await next_link.click()

                await page.wait_for_function(
                    """previousRow => {
                        const row = document.querySelector("tbody tr");
                        return row && row.innerText.trim() !== previousRow;
                    }""",
                    arg=first_row_before,
                    timeout=30_000,
                )
                
        finally:
            # Close the Playwright page after scraping all results.
            await page.close()

    def parse_agent_page(self, response):
        agent_item = AgentItem()

        agent_item["first_name"] = response.meta.get("first_name")
        agent_item["last_name"] = response.meta.get("last_name")

        agent_item["email_address"] = response.xpath(
            '//tr[td[contains(normalize-space(), "Email address")]]'
            '/td[2]/a[starts-with(@href, "mailto:")]/text()'
        ).get()

        yield agent_item