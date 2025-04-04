from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from portfolio.unfold_navigation import PAGES

def environment_callback(request):
    if settings.DEBUG:
        return [_("Development"), "warning"]
    return [_("Production"), "success"]

UNFOLD = {
    "SITE_TITLE": "Abdulaziz Portfolio",
    "SITE_HEADER": "Portfolio Admin",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/logo-light.png"),
        "dark": lambda request: static("images/logo-dark.png"),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "href": lambda request: static("images/favicon.ico"),
        },
    ],
    "SITE_SYMBOL": "dashboard",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "portfolio.admin_config.environment_callback",
    "DASHBOARD_CALLBACK": "portfolio.dashboard.dashboard_stats",
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),
        "title": "Abdulaziz Portfolio",
        "subtitle": "Admin Panel",
        "greeting": "Welcome back",
    },
    "STYLES": [
        lambda request: static("css/admin-custom.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/admin-custom.js"),
    ],
    "BORDER_RADIUS": "12px",
    "THEME": {
        "DEFAULT": "light",
        "SWITCHER": True
    },
    "COLORS": {
        "base": {
            "50": "202 210 224",
            "100": "172 180 194",
            "200": "142 150 164",
            "300": "112 120 134",
            "400": "82 90 104",
            "500": "52 60 74",
            "600": "42 50 64",
            "700": "32 40 54",
            "800": "22 30 44",
            "900": "12 20 34",
            "950": "8 16 28",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
        "primary": {
            "50": "230 243 240",
            "100": "184 241 231",
            "200": "133 236 218",
            "300": "74 224 202",
            "400": "35 202 181",
            "500": "10 174 156",
            "600": "9 138 126",
            "700": "11 108 100",
            "800": "13 84 79",
            "900": "15 68 64",
            "950": "0 37 36",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
    },
    "TABS": [
        {
            "name": "dashboard",
            "models": [
                "blog.post",
                "projects.project",
            ],
            "items": [
                {
                    "app": "blog",
                    "model": "post",
                    "text": _("Posts"),
                    "link": lambda request: "blog/post/",
                    "items": [
                        {
                            "text": _("All"),
                            "attr": {"class": "flex"},
                            "permission": "blog.view_post",
                            "link": lambda request: "blog/post/",
                        },
                        {
                            "text": _("Recently Added"),
                            "permission": "blog.view_post",
                            "link": lambda request: "blog/post/?created_days=7",
                        },
                        {
                            "text": _("Popular"),
                            "permission": "blog.view_post",
                            "link": lambda request: "blog/post/?views_gt=10",
                        },
                    ],
                },
                {
                    "app": "projects",
                    "model": "project",
                    "text": _("Projects"),
                    "link": lambda request: "projects/project/",
                    "items": [
                        {
                            "text": _("All"),
                            "permission": "projects.view_project",
                            "link": lambda request: "projects/project/",
                        },
                        {
                            "text": _("Featured"),
                            "permission": "projects.view_project",
                            "link": lambda request: "projects/project/?featured=1",
                        },
                    ],
                },
            ]
        }
    ],
    "FIELDS": {
        "TextField": {
            "rows": 8,
            "class": "custom-textfield",
        },
        "URLField": {
            "class": "custom-url-field",
        },
        "SplitDateTimeField": {
            "class": "custom-datetime-field",
        },
    },
    "API_VIEWER": {
        "default": "https://api.abdulaziz.org.uz/api/", 
        "routes": [
            {
                "text": "Posts",
                "endpoint": "posts/",
            },
            {
                "text": "Projects",
                "endpoint": "projects/",
            },
            {
                "text": "Skills",
                "endpoint": "skills/",
            },
            {
                "text": "Telegraph API",
                "endpoint": "telegraph/page-info/",
            },
        ],
    },
} 