$industries = @("Accountancy", "Actuarial", "Admin", "Banking", "Construction", "Customer Service", "Education", "Energy", "Engineering ", "Estate Agency", "Financial", "Insurance", "Health", "Hospitality", "Human Resources", "IT ", "Journalism", "Legal", "Tourism", "Logistics", "Manufacturing", "Management ", "Marketing", "Media", "Automotive", "Multilingual", "Purchasing ", "Quantity surveying", "Retail", "Sales", "Science", "Security", "Social Care", "Teaching", "Training", "Transport")

foreach ($i in $industries){
    scrapy crawl indeed -a l="Dundee" -a q=$i
}
    
scrapy crawl facebook -a start_page_id=282183438466910
scrapy crawl twitter_dundee_jcp
