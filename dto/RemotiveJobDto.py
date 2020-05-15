import json

from dto.BaseJobDto import BaseJobDto
from util.str_util import auto_str, no_html_tags_text
from util.json_util import to_obj


@auto_str
class RemotiveJobDto(BaseJobDto):
    def __init__(self, tags=None, job_type=None, publication_date=None,
                 candidate_required_location=None, salary=None, company_logo_url=None):
        super().__init__()
        self.companyLogoUrl = company_logo_url
        self.salary = salary
        self.candidateRequiredLocation = candidate_required_location
        self.publicationDate = publication_date
        self.jobType = job_type
        self.tags = tags

    def get_cleaned_description(self):
        self.description_text = no_html_tags_text(self.description)


if __name__ == '__main__':
    json_str = json.dumps({"candidateRequiredLocation":"","category":"Software Development","companyName":"Carbon Relay","description":"<p>Carbon Relay is a world-class team focused on harnessing the power of machine learning to optimize Kubernetes. Our innovative platform allows organizations to boost application performance while keeping costs down. We recently completed a <a href=\"https://www.carbonrelay.com/news/carbon-relay-raises-63-million/\" rel=\"nofollow\">major fundraising round</a> and are scaling up rapidly to turn our vision into reality. This position is perfect for someone who wants to get in on the ground floor at a startup that moves fast, tackles hard problems, and has fun!</p><p>We are looking for a Lead Software Engineer to spearhead the development of our backend applications. You will bridge the gap between the machine learning and Kubernetes teams to ensure that our products delight customers and scale efficiently.</p><p><strong>Responsibilities</strong></p><ul><li>Developing our internal APIs and backend</li><br><li>Designing and implementing SaaS-based microservices</li><br><li>Collaborating with our infrastructure, machine learning and Kubernetes teams</li></ul><p><strong>Required qualifications</strong></p><ul><li>10 + years experience in software engineering</li><br><li>Proficiency in Python</li><br><li>Experience shipping and maintaining software products</li></ul><p><strong>Preferred qualifications</strong></p><ul><li>Experience with JavaScript</li><br><li>Experience with GCP/GKE</li><br><li>Familiarity with Kubernetes and containerization</li></ul><p><strong>Why join Carbon Relay</strong></p><ul><li>Competitive salary</li><br><li>Health, dental, vision and life insurance</li><br><li>Unlimited vacation policy (and we do really take vacations)</li><br><li>Ability to work remotely</li><br><li>Snacks, lunches and all the typical benefits you would expect from a well-funded, fun startup!</li><br></ul>","id":"87441","jobType":"full_time","publicationDate":"2020-02-15T10:22:47","salary":"","tags":["python","rest","flask"],"title":"Lead Software Engineer","url":"https://remotive.io/remote-jobs/software-dev/lead-software-engineer-87441"})
    remotive_job = to_obj(RemotiveJobDto(), json_str)
    print(remotive_job)