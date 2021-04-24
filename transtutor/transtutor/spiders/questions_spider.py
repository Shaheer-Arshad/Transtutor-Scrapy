import scrapy

class Questions(scrapy.Spider):
    name="transtutor"
    start_urls = [
        'https://www.transtutors.com/questions/writing/'
    ]

    def parse(self, response): #This gets the subcateogry of the subject
        
        in_ui = response.css("ul.ltwo>li")

        for a in in_ui:
            sub_link= "https://www.transtutors.com" + a.css("a::attr(href)").get()
            yield scrapy.Request(url=sub_link,callback=self.subject_category)
    

    def subject_category(self, response): # This checks total pages of categories

        total_pages= response.xpath("/html/body/form/section/div[2]/div[2]/div[2]/a[12]/@href").get().split('/')[-2]

        for i in range(int(total_pages)+1):
            link = response.request.url+str(i)
            yield scrapy.Request(url=link,callback=self.pages)

    def pages(self,response): # this goes to question page
        
        ul = response.css("ul.inner-topics-covered li")
        for b in ul:
            question_link = b.css("a::attr(href)").get()
            yield scrapy.Request(url=question_link,callback=self.parse_question)


    def parse_question(self, response): # this collects data from question

        category = response.xpath("/html/body/form/div[2]/div/section/div[3]/div[1]/div[1]/ol/li[3]/a/span/text()").get()
        subcategory = response.xpath("/html/body/form/div[2]/div/section/div[3]/div[1]/div[1]/ol/li[4]/a/span/text()").get()
        title = response.xpath("/html/body/form/div[2]/div/section/div[3]/div[3]/div[1]/div[1]/h1/text()").getall()
        question = response.css("#divDescription ::text").getall()
        date= response.css("#spnQuestionSubmittedDate::text").get()


        li2=' '.join(title)
        li3=' '.join(question)

        yield {
            "Date":date,
            "Cateogry":category,
            "Sub-Category":subcategory,
            "Title":li2.strip(),
            "Question":li3.strip(),
                }
        
