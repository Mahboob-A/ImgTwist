import json

from rest_framework.renderers import JSONRenderer


class ProductJSONRenderer(JSONRenderer):
    """Renderer class for Product."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        else:
            status_code = renderer_context.get("response").status_code

        if data is not None:
            errors = data.get("errors", None)
        else:
            errors = None

        if errors is not None:
            return super(ProductJSONRenderer, self).render(data)
        else:
            return json.dumps({"status_code": status_code, "product": data})


class ProductsJSONRenderer(JSONRenderer):
    """Renderer class for Product QuerySet."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        else:
            status_code = renderer_context.get("response").status_code

        if isinstance(data, dict):
            errors = data.get("errors", None)
            if errors is not None:
                return super(ProductsJSONRenderer, self).render(data)

        return json.dumps({"status_code": status_code, "products": data})
