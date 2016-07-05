from scrapy.item import Item, Field

class LearningResource(Item):

    #title = Field()
    name = Field()
    identifier = Field()
    #description = Field()
    url = Field()
    typeOfResource = Field() 
    language = Field() 
    
    prerequisites = Field()
    
    #subject = Field()
    #topic = Field()
    #about = Field()
    
    #keywords = Field()
    #tags = Field()             
    
    #creator = Agent()
    
    #educationLevel = Field()
    #audience = Field()
    
    #typicalAgeRange = Field()

    #dateCreated = Field()
    #dateModified = Field()
    datePublished = Field()
    #available  = Field()
    
    #contactHours = Field()
    #studyHours = Field()
    
    #schema:review            A review of the item.
    #schema:price            schema:PriceSpecification 

    version = Field()
    
    #languageOfInstruction = Field()
    #languageOfAssessment = Field()

    #format = Field()
    
    #location = Field()

    #dcterms:license        dcterms:LicenseDocument      (creative commons, MIT open courseware, ...)
    #dcterms:rights        dcterms:Agent ( person or organization owning or managing rights over the resource. )
    #dcterms:rightsHolder
    #schema:copyrightHolder
    #dcterms:accessRights
    
    #dcterms:publisher    dcterm:Agent  (e.g., Coursera, ...) 
    provider = Field() 
    
class Agent(Item):
    
    name = Field()
    
