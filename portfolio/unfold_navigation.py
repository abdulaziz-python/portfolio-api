from django.utils.translation import gettext_lazy as _

PAGES = [
    {
        "name": _("Dashboard"),
        "url": "admin:index",
        "icon": "home",
    },
    {
        "name": _("Blog"),
        "icon": "edit_note",
        "models": [
            {
                "name": _("Posts"),
                "url": "admin:blog_post_changelist",
                "icon": "article",
                "add_url": "admin:blog_post_add",
                "add_name": _("Add Post"),
            },
            {
                "name": _("Comments"),
                "url": "admin:blog_comment_changelist",
                "icon": "question_answer",
                "add_url": "admin:blog_comment_add",
                "add_name": _("Add Comment"),
            },
        ],
    },
    {
        "name": _("Projects"),
        "icon": "work",
        "models": [
            {
                "name": _("Projects"),
                "url": "admin:projects_project_changelist",
                "icon": "folder",
                "add_url": "admin:projects_project_add",
                "add_name": _("Add Project"),
            },
            {
                "name": _("Skills"),
                "url": "admin:projects_skill_changelist",
                "icon": "tune",
                "add_url": "admin:projects_skill_add",
                "add_name": _("Add Skill"),
            },
        ],
    },
    {
        "name": _("API"),
        "icon": "api",
        "url": "api-root",
        "target": "_blank",
    },
    {
        "name": _("Telegraph"),
        "icon": "cloud_upload",
        "models": [
            {
                "name": _("Pages"),
                "url": "telegraph-pages",
                "icon": "pages",
            },
            {
                "name": _("Upload Image"),
                "url": "telegraph-upload",
                "icon": "upload_file",
            },
        ],
    },
    {
        "name": _("Auth"),
        "icon": "admin_panel_settings",
        "models": [
            {
                "name": _("Users"),
                "url": "admin:auth_user_changelist",
                "icon": "people",
                "add_url": "admin:auth_user_add",
                "add_name": _("Add User"),
            },
            {
                "name": _("Groups"),
                "url": "admin:auth_group_changelist",
                "icon": "group",
                "add_url": "admin:auth_group_add",
                "add_name": _("Add Group"),
            },
        ],
    },
    {
        "name": _("Settings"),
        "url": "admin:password_change",
        "icon": "settings",
    },
] 