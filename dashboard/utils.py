import os
import random
from datetime import datetime
from io import BytesIO
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from weasyprint import HTML
from xhtml2pdf import pisa
from weasyprint.fonts import FontConfiguration


def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = '1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(3))
    year = datetime.now().year
    month = datetime.now().month
    directory = instance.folder
    return '{path}/{year}/{month}/{basename}-{randomstring}{ext}'.format(year=year,
                                                                         month=month, basename=basefilename, randomstring=randomstr, ext=file_extension, path=directory)


def ref_code_generator():
    chars = '1234567890FEYTONFABRUCE'
    randomstr = ''.join((random.choice(chars)) for x in range(5))
    date, month = datetime.now().date(), datetime.now().month
    return '%s-%s-%s' % (month, date, randomstr)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def generate_pdf_weasy(request, template, file_name, context):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=%s.pdf" % (file_name)
    html = render_to_string(template, context)

    font_config = FontConfiguration()
    pdf = HTML(string=html, base_url=request.build_absolute_uri()
               ).write_pdf(response, font_config=font_config)
    return response
