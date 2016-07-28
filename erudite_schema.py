class Bio:
	"""
	 The biography of the instructor 
	"""
	bio = 'bio'

	bio_owner = Instructor()


	def __init__(self):
		pass


"""
 A Provider is an organization that generates and supports a LearningResource. 
 
"""
class Provider:
	id = 'id'

	"""
	 The name of the provider. 
	"""
	name = 'name'

	"""
	 A description of the provider. 
	"""
	description = 'description'

	"""
	 An alternate name for the provider 
	"""
	alternate_name = 'alternate_name'

	"""
	 Which country is the provider located in? 
	"""
	country = 'country'

	"""
	 Which city is the provider located in? 
	"""
	city = 'city'

	"""
	 Which state is the provider located in? 
	"""
	state = 'state'

	"""
	 The latitude of the provider. 
	"""
	latitude = 'latitude'

	"""
	 A URL where the provider is found online 
	"""
	url = 'url'

	provides = provides()

	is_worker = is_worker()


	def __init__(self):
		pass


"""
 An Instructor is an individual who facilitates the delivery of 
 a LearningResource to students. 
"""
class Instructor:
	id = 'id'

	"""
	 First name of the instructor 
	"""
	first_name = 'first_name'

	"""
	 Middle name of the instructor 
	"""
	middle_name = 'middle_name'

	"""
	 Last name of the instructor 
	"""
	last_name = 'last_name'

	"""
	 Full name of the instructor 
	"""
	full_name = 'full_name'

	"""
	 Short name of the instructor 
	"""
	short_name = 'short_name'

	"""
	 Job title of the instructor 
	"""
	job_title = 'job_title'

	has_bio = has_bio()

	works_for = works_for()

	teaches = teaches()


	def __init__(self):
		pass


"""
 Tags are designated as ontological labels associated with Learning 
 Resources. 
"""
class Tag:
	"""
	 What is the tag? 
	"""
	concept_tag = 'concept_tag'

	tagged = tagged()


	def __init__(self):
		pass


"""
 A learning resource could be an MOOC course or program, a university 
 course or program, a tutorial document, a textbook or any other 
 digital resource that has a pedagogical purpose and is indexed 
 in our system. 
"""
class LearningResource:
	"""
	 Title of the resource 
	"""
	title = 'title'

	"""
	 Any subtitles that the resource might have 
	"""
	subtitle = 'subtitle'

	"""
	 Discription of the resource (usually a paragraph or two from 
	 a course catalog) 
	"""
	description = 'description'

	"""
	 Simple one or two line description of the resource 
	"""
	short_description = 'short_description'

	"""
	 A description of the contents of the course written in text 
	"""
	syllabus = 'syllabus'

	"""
	 A URL where the resource is found online 
	"""
	url = 'url'

	"""
	 The stem of the URL where this resource may be found within the 
	 provider's website 
	"""
	slug = 'slug'

	"""
	 A string describing the prequesites of this resource 
	"""
	prerequisite = 'prerequisite'

	"""
	 The education level needed to study this resource. 
	"""
	education_level = 'education_level'

	"""
	 When was this resource created? 
	"""
	created = 'created'

	"""
	 When was this resource last modified? 
	"""
	date_modified = 'date_modified'

	"""
	 When will this resource be available? 
	"""
	available = 'available'

	"""
	 When will this resource no longer be available? 
	"""
	end_date = 'end_date'

	"""
	 How long does it typically take for a student to process the 
	 material in this resource? 
	"""
	typical_learning_time = 'typical_learning_time'

	"""
	 What is this resource's rating (of quality) 
	"""
	rating = 'rating'

	"""
	 What is the cost a student would pay to learn this resource. 
	 
	"""
	price = 'price'

	"""
	 What t 
	"""
	has_version = 'has_version'

	"""
	 Is this a new course? 
	"""
	new = 'new'

	"""
	 What language is the resource written in? 
	"""
	language = 'language'

	"""
	 What is the format of the resource 
	"""
	format = 'format'

	"""
	 What is the license that covers this resource's usage? 
	"""
	license = 'license'

	venue = 'venue'

	is_teacher = is_teacher()

	has_tag = has_tag()

	provider = provider()


	def __init__(self):
		pass
