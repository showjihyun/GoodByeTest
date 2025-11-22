import gitlab
import os

class GitLabClient:
    def __init__(self, url='https://gitlab.com', private_token=None, project_id=None):
        self.gl = gitlab.Gitlab(url, private_token=private_token)
        self.project_id = project_id
        self.project = self.gl.projects.get(self.project_id) if self.project_id else None

    def get_merge_request(self, mr_iid):
        if not self.project:
            raise ValueError("Project not initialized")
        return self.project.mergerequests.get(mr_iid)

    def get_mr_changes(self, mr_iid):
        mr = self.get_merge_request(mr_iid)
        return mr.changes()

    def post_comment(self, mr_iid, body):
        mr = self.get_merge_request(mr_iid)
        mr.notes.create({'body': body})

    def post_discussion(self, mr_iid, body, position=None):
        """
        Post a threaded discussion.
        position: dict with 'base_sha', 'start_sha', 'head_sha', 'position_type', 'new_path', 'new_line' etc.
        """
        mr = self.get_merge_request(mr_iid)
        mr.discussions.create({'body': body, 'position': position})
