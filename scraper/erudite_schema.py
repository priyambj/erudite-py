from pprint import pprint


class Provider:
    """
     A Provider is an organization that generates and supports a LearningResource.

    """

    """
     The name of the provider
    """

    id = ''

    """
     The name of the provider.
    """
    name = ''

    """
     A description of the provider.
    """
    description = ''

    """
     An alternate name for the provider
    """
    alternate_name = ''

    """
     Which country is the provider located in?
    """
    country = ''

    """
     Which city is the provider located in?
    """
    city = ''

    """
     Which state is the provider located in?
    """
    state = ''

    """
     The latitude of the provider.
    """
    latitude = 0.0

    """
     A URL where the provider is found online
    """
    url = ''

    provides = []

    is_worker = []

    def __init__(self):
        pass


class Instructor:
    """
     An Instructor is an individual who facilitates the delivery of
     a LearningResource to students.
    """

    """
     Full name of the instructor
    """
    id = ''

    """
     First name of the instructor
    """
    first_name = ''

    """
     Middle name of the instructor
    """
    middle_name = ''

    """
     Last name of the instructor
    """
    last_name = ''

    """
     Full name of the instructor
    """
    full_name = ''

    """
     Short name of the instructor
    """
    short_name = ''

    """
     Job title of the instructor
    """
    job_title = ''

    has_bio = set()

    works_for = set()

    teaches = set()

    def __init__(self):
        pass

    def __hash__(self):
        return hash(self.id)

    def print_info(self):
        pprint(vars(self))


class Bio:
    """
     The biography of the instructor
    """

    """
     Url of the biography
    """
    id = ''

    """
     The biography itself.
    """
    bio = ''

    """
     Owner of the biography.
    """
    bio_owner = Instructor()

    """
     Url of the biography
    """
    url = ''

    def __init__(self):
        pass

    def __hash__(self):
        return hash(self.id)

    def print_info(self):
        pprint(vars(self))


class Tag:
    """
     Tags are designated as ontological labels associated with Learning
     Resources.
    """

    """
     What is the tag?
    """
    concept_tag = ''

    """
     Set of resource ids tagged with this tag.
    """
    tagged = set()

    def __init__(self):
        pass

    def __hash__(self):
        return hash(self.concept_tag)

    def print_info(self):
        pprint(vars(self))


class LearningResource:
    """
     A learning resource could be an MOOC course or program, a university
     course or program, a tutorial document, a textbook or any other
     digital resource that has a pedagogical purpose and is indexed
     in our system.
    """

    """
     Url of the resource.
    """
    id = ''

    """
     Title of the resource
    """
    title = ''

    """
     Any subtitles that the resource might have
    """
    subtitle = ''

    """
     Discription of the resource (usually a paragraph or two from
     a course catalog)
    """
    description = ''

    """
     Simple one or two line description of the resource
    """
    short_description = ''

    """
     A description of the contents of the course written in text
    """
    syllabus = ''

    """
     A URL where the resource is found online
    """
    url = ''

    """
     The stem of the URL where this resource may be found within the
     provider's website
    """
    slug = ''

    """
     A string describing the perquisites of this resource
    """
    prerequisite = ''

    """
     The education level needed to study this resource.
    """
    education_level = ''

    """
     When was this resource created?
    """
    created = ''

    """
     When was this resource last modified?
    """
    date_modified = ''

    """
     When will this resource be available?
    """
    available = ''

    """
     When will this resource no longer be available?
    """
    end_date = ''

    """
     How long does it typically take for a student to process the
     material in this resource?
    """
    typical_learning_time = ''

    """
     What is this resource's rating (of quality)
    """
    rating = ''

    """
     What is the cost a student would pay to learn this resource.

    """
    price = ''

    """
     Version of the resource
    """
    has_version = ''

    """
     Is this a new course?
    """
    new = ''

    """
     What language is the resource written in?
    """
    language = ''

    """
     What is the format of the resource
    """
    format = ''

    """
     What is the license that covers this resource's usage?
    """
    license = ''

    """
     Ordered Course-ids (urls) of a series, specialization etc.
    """
    courses = list()

    venue = ''

    is_teacher = set()

    has_tag = set()

    provider = set()

    objectives = ''

    length = ''

    def __init__(self):
        pass

    def __hash__(self):
        return hash(self.id)

    def print_info(self):
        pprint(vars(self))
