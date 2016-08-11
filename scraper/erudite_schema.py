from pprint import pprint


class Provider:
    """
     A Provider is an organization that generates and supports a LearningResource.

    """

    db_fields = ['id', 'name', 'description', 'alternate_name', 'city', 'state',
                 'latitude', 'url']

    def __init__(self):
        """
         Init all members to default values
        """

        """
         The name of the provider
        """
        self.id = ''

        """
         The name of the provider.
        """
        self.name = ''

        """
         A description of the provider.
        """
        self.description = ''

        """
         An alternate name for the provider
        """
        self.alternate_name = ''

        """
         Which country is the provider located in?
        """
        self.country = ''

        """
         Which city is the provider located in?
        """
        self.city = ''

        """
         Which state is the provider located in?
        """
        self.state = ''

        """
         The latitude of the provider.
        """
        self.latitude = ''

        """
         A URL where the provider is found online
        """
        self.url = ''

    def __bool__(self):
        return self.id != ''

    def __hash__(self):
        return hash(self.id)

    def print_info(self):
        pprint(vars(self))

    def __str__(self):
        return self.id


class Instructor:
    """
     An Instructor is an individual who facilitates the delivery of
     a LearningResource to students.
    """

    db_fields = ['id', 'first_name', 'middle_name', 'last_name', 'full_name', 'short_name', 'job_title', 'works_for']

    def __init__(self):
        """
         Init all members to default values
        """

        """
         Full name of the instructor
        """
        self.id = ''

        """
         First name of the instructor
        """
        self.first_name = ''

        """
         Middle name of the instructor
        """
        self.middle_name = ''

        """
         Last name of the instructor
        """
        self.last_name = ''

        """
         Full name of the instructor
        """
        self.full_name = ''

        """
         Short name of the instructor
        """
        self.short_name = ''

        """
         Job title of the instructor
        """
        self.job_title = ''

        self.biography = set()

        self.works_for = set()

        self.teaches = set()

    def __hash__(self):
        return hash(self.id)

    def print_info(self):
        pprint(vars(self))

    def __bool__(self):
        return self.id != ''


class Bio:
    """
     The biography of the instructor
    """

    db_fields = ['instructor_id', 'bio']

    def __init__(self):
        """
         Init all members to default values
        """

        """
         Url of the biography
        """
        self.id = ''

        """
         The biography itself.
        """
        self.bio = ''

        """
         Owner of the biography.
        """
        self.instructor_id = ''

        """
         Url of the biography
        """
        self.url = ''

    def __init__(self):
        pass

    def __hash__(self):
        return hash(self.id)

    def print_info(self):
        pprint(vars(self))

    def __bool__(self):
        return self.bio != '' and len(self.bio) > 10


class Tag:
    """
     Tags are designated as ontological labels associated with Learning
     Resources.
    """

    def __init__(self):
        """
         Init all members to default values
        """

        """
         What is the tag?
        """
        self.concept_tag = ''

        """
         Set of resource ids tagged with this tag.
        """
        self.tagged = set()

    def __hash__(self):
        return hash(self.concept_tag)

    def print_info(self):
        pprint(vars(self))

    def __bool__(self):
        return self.concept_tag != ''


class LearningResource:
    """
     A learning resource could be an MOOC course or program, a university
     course or program, a tutorial document, a textbook or any other
     digital resource that has a pedagogical purpose and is indexed
     in our system.
    """

    db_fields = ['id', 'title', 'subtitle', 'description', 'short_description', 'syllabus',
                 'url', 'slug', 'difficulty', 'created', 'date_modified', 'end_date', 'typical_learning_time',
                 'rating', 'price', 'new', 'language', 'format', 'license', 'venue']

    def __init__(self):
        """
         Init all members to default values
        """

        """
         Url of the resource.
        """
        self.id = ''

        """
         Title of the resource
        """
        self.title = ''

        """
         Any subtitles that the resource might have
        """
        self.subtitle = ''

        """
         Discription of the resource (usually a paragraph or two from
         a course catalog)
        """
        self.description = ''

        """
         Simple one or two line description of the resource
        """
        self.short_description = ''

        """
         A description of the contents of the course written in text
        """
        self.syllabus = ''

        """
         A URL where the resource is found online
        """
        self.url = ''

        """
         The stem of the URL where this resource may be found within the
         provider's website
        """
        self.slug = ''

        """
         A string describing the perquisites of this resource
        """
        self.prerequisite = ''

        """
         The education level needed to study this resource.
        """
        self.difficulty = ''

        """
         When was this resource created?
        """
        self.created = ''

        """
         When was this resource last modified?
        """
        self.date_modified = ''

        """
         When will this resource be available?
        """
        self.available = ''

        """
         When will this resource no longer be available?
        """
        self.end_date = ''

        """
         How long does it typically take for a student to process the
         material in this resource?
        """
        self.typical_learning_time = ''

        """
         What is this resource's rating (of quality)
        """
        self.rating = ''

        """
         What is the cost a student would pay to learn this resource.

        """
        self.price = ''

        """
         Version of the resource
        """
        self.has_version = ''

        """
         Is this a new course?
        """
        self.new = ''

        """
         What language is the resource written in?
        """
        self.language = ''

        """
         What is the format of the resource
        """
        self.format = ''

        """
         What is the license that covers this resource's usage?
        """
        self.license = ''

        self.venue = ''

        self.objectives = ''

        self.length = ''

        """
         Ordered Course-ids (urls) of a series, specialization etc.
        """
        self.courses = list()
        """
         Set of Instructor instances.
        """
        self.instructors = set()
        """
         Set of Tag instances.
        """
        self.tags = set()
        """
         Provider instances of the provider (see class Provider)
        """
        self.provider = Provider()

    def __hash__(self):
        return hash(self.id)

    def print_info(self):
        pprint(vars(self))

    def __bool__(self):
        return self.id != ''




