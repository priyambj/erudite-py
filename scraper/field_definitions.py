class Fields:
    # We need a good definition of each field here and keep it up to date
    resource_type = 'type'
    """
    The type of the resource. Valid values include:
        * course: a course about a topic
        * video: a single video about a topic
    """

    title = 'title'
    """
    The title of the course
    """

    subtitle = 'subtitle'
    """
    The subtitle of a course.
    """

    description = 'description'
    """
    The description/summary of a course.
    """

    short_description = 'short_description'
    """
    The short description/summary of a course.
    """

    syllabus = 'syllabus'
    """
    The syllabus of the course
    """

    part_of = 'part_of'
    """
    If the course is e.g. part of a specialization or a video part of a course. I guess we should talk about how we
    are going to handle this.
    """

    index = 'index'
    """
    Index of a resource within its parent. E.g.: Index of a course within it's specialization.
    """

    def __init__(self):
        pass