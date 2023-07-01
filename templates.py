import json
from typing import Any, Dict, List, Optional, Set, Tuple, Union

templates = {
    "gpt-4_default": {
        "chat_log": {
            "model": "gpt-4",
            "max_model_tokens": 8000,
            "max_completion_tokens": 1000,
            "max_chat_messages": 1000,
            "token_padding": 500,
        },
        "gpt_chat": {
            "model_name": "gpt-4",
            "max_tokens": 1000,
            "temperature": 1.1,
            "top_p": 1.0,
            "frequency_penalty": 0.5,
        },
        "description": "Default settings for gpt-4",
        "tags": ["gpt-4", "default", "normal"],
    },
    "gpt-4_small": {
        "chat_log": {
            "model": "gpt-4",
            "max_model_tokens": 8000,
            "max_completion_tokens": 1000,
            "max_chat_messages": 50,
            "token_padding": 500,
        },
        "gpt_chat": {
            "model_name": "gpt-4",
            "max_tokens": 1000,
            "temperature": 0.5,
            "top_p": 1.0,
        },
        "description": "To save money on tokens use this to limit the number of messages to 50",
        "tags": ["gpt-4", "small", "cheap", "low-cost"],
    },
    "gpt-4_creative": {
        "chat_log": {
            "model": "gpt-4",
            "max_model_tokens": 8000,
            "max_completion_tokens": 1000,
            "max_chat_messages": 1000,
            "token_padding": 500,
        },
        "gpt_chat": {
            "model_name": "gpt-4",
            "max_tokens": 1000,
            "temperature": 1.5,
        },
        "description": "Use this to get more creative responses, higher temperature means more creative",
        "tags": ["gpt-4", "creative", "high-temperature"],
    },
    "gpt-3_16K_default": {
        "chat_log": {
            "model": "gpt-3",
            "max_model_tokens": 16000,
            "max_completion_tokens": 2000,
            "max_chat_messages": 2000,
            "token_padding": 500,
        },
        "gpt_chat": {
            "model_name": "gpt-3-16K",
            "max_tokens": 2000,
            "temperature": 0.5,
        },
        "description": "Default settings for gpt-3-16K",
        "tags": ["gpt-3-16K", "default", "normal", "gpt-3"],
    },
}


def get_template_from_file(file_path: str = "templates.json") -> dict:
    with open(file_path, "r") as f:
        templates = json.load(f)
    return templates





class GetTemplates:
    
    """Class to manage templates and provide a simple interface to get templates
    Methods:
        __init__(templates: dict) -> None
        get_template(template_name: str) -> dict
        search_templates_by_tag(tag: str, return_type = "name") -> list[dict]| list[str]
        get_template_part(template_name: str, part: str) -> dict| str | list
    Attributes:
        templates: dict
    Raises:
        TemplateNotFoundError
        ValueError
    Dependencies:
        json
    Example Usage:
        templates = {
            "template_name": {
                "chat_log": { "model": "gpt-4", "max_model_tokens": 8000, "max_completion_tokens": 1000, "max_chat_messages": 1000, "token_padding": 500, },
                "gpt_chat": { "model_name": "gpt-4", "max_tokens": 1000, "temperature": 1.1, "top_p": 1.0, "frequency_penalty": 0.5, },
                "description": "Default settings for gpt-4",
                "tags" : ["gpt-4", "default", "normal"],
            },...
            }
        template_manager = GetTemplates(templates)
        template_names = template_manager.search_templates_by_tag("gpt-4", return_type="name")
        template = template_manager.get_template(template_names[0])

    """

    def __init__(self, templates: dict):
        for name, template in templates.items():
            self._verify_single_template(template_name=name, template=template)
        self.templates = templates

    required_top_level_keys = {"chat_log", "gpt_chat", "description", "tags"}

    def get_template(self, template_name: str) -> dict:
        """Get a template by name"""
        if template_name not in self.templates:
            raise self.TemplateNotFoundError(template_name=template_name)
        return self.templates[template_name]

    def search_templates_by_tag(
        self, tag: str, return_type: str = "name"
    ) -> Union[List[Dict], List[str]]:
        """Search templates by tag"""
        allowed_return_types = ["list", "name"]
        if return_type not in allowed_return_types:
            raise ValueError(f"return_type must be one of {allowed_return_types}")

        if return_type == "list":
            result = [
                template
                for template in self.templates.values()
                if tag in template["tags"]
            ]
        elif return_type == "name":
            result = [
                name
                for name, template in self.templates.items()
                if tag in template["tags"]
            ]

        return result

    def _verify_templates(self, templates: dict) -> dict:
        """Verify that a template is valid, raises BadTemplateError if not. Return the template if valid"""
        if not isinstance(templates, dict):
            raise self.BadTemplateError("Templates must be a dict")

        if not self.required_top_level_keys == set(templates.keys()):
            for template_name, template in templates.items():
                self._verify_single_template(
                    template_name=template_name, template=template
                )
        else:
            return self._verify_single_template(templates)

        return templates

    def _verify_single_template(self, template_name: str, template: dict) -> dict:
        """Verify that a template is valid, raises BadTemplateError if not. Return the template if valid"""
        allowed_chat_log_keys = {
            "model",
            "max_model_tokens",
            "max_completion_tokens",
            "max_chat_messages",
            "token_padding",
        }
        allowed_gpt_chat_keys = {
            "model_name",
            "max_tokens",
            "temperature",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
        }

        if not isinstance(template, dict):
            raise self.BadTemplateError(f"Template '{template_name}' must be a dict")
        if self.required_top_level_keys != set(template.keys()):
            msg = f"Template '{template_name}' must have the following keys: {self.required_top_level_keys}, missing {self.required_top_level_keys.symmetric_difference( set(template.keys()))} "
            raise self.BadTemplateError(msg)
        if not isinstance(template["chat_log"], dict):
            raise self.BadTemplateError(
                f"'chat_log' in template '{template_name}' must be a dict"
            )

        if not isinstance(template["gpt_chat"], dict):
            raise self.BadTemplateError(
                f"'gpt_chat' in template '{template_name}' must be a dict"
            )

        chat_dif = set(template["chat_log"].keys()) - allowed_chat_log_keys

        if len(chat_dif) > 0:
            raise self.BadTemplateError(
                f"'chat_log' keys in template '{template_name}' must be one of {allowed_chat_log_keys}. Got {chat_dif}"
            )

        gpt_dif = set(template["gpt_chat"].keys()) - allowed_gpt_chat_keys
        if len(gpt_dif) > 0:
            raise self.BadTemplateError(
                f"'gpt_chat' keys in template '{template_name}' must be one of {allowed_gpt_chat_keys}. Got {gpt_dif}"
            )

        if not isinstance(template["description"], str):
            raise self.BadTemplateError(
                f"'description' in template '{template_name}' must be a str"
            )

        if not isinstance(template["tags"], list):
            raise self.BadTemplateError(
                f"'tags' in template '{template_name}' must be a list"
            )

        return template

    def get_template_part(self, template_name: str, part: str) -> dict | str | list:
        """Get a part of a template by name"""

        allowed_parts = ["chat_log", "gpt_chat", "description", "tags"]
        if part not in allowed_parts:
            raise ValueError(f"part must be one of {allowed_parts}")
        if template_name not in self.templates.keys():
            raise self.TemplateNotFoundError(template_name=template_name)
        return self.templates[template_name][part]
    def get_all_templates_names(self, include_tags: bool = False, include_descriptions: bool = False) -> list[str] | list[dict]:
        result = []
        for name in self.templates.keys():
            if include_tags or include_descriptions:
                item = {"name": name}
                if include_tags:
                    item.update({"tags": self.templates[name]["tags"]})
                if include_descriptions:
                    item.update({"description": self.templates[name]["description"]})
            else:
                item = name
            result.append(item)
            return result
        
    def get_template_info(self, template_name: str) -> dict:
        result = {}
        try: 
            template = self.get_template(template_name)
            result.update({"name": template_name, "description": template["description"], "tags": template["tags"]})
        except self.TemplateNotFoundError:
            result = {"name": template_name, "error": "Template not found"}
        return result
            
    def get_template(self, template_name):
        if template_name not in self.templates.keys():
            raise self.TemplateNotFoundError(template_name=template_name)
        return self.templates[template_name]

    class TemplateNotFoundError(Exception):
        def __init__(self, message=None, template_name: str = None):
            if message is None:
                message = "Template not found"
            if template_name is not None:
                message = f"{message} \n Template {template_name} not found"

        def __str__(self):
            return self.message


    class BadTemplateError(Exception):
        def __init__(self, message: str = None):
            if message is None:
                message = "Template is not valid"
            self.message = message

        def __str__(self):
            return self.message
template_selector = GetTemplates(templates)
