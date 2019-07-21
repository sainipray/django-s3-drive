from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from main.storage import PrivateS3Storage


class ListS3View(TemplateView):
	template_name = 'cloud.html'
	storage = PrivateS3Storage()

	def get_nav(self):
		directory = self.get_directory()
		urls = []
		dirs = directory.split('/') if directory else []
		for index, dir in enumerate(dirs):
			urls.append({'name': dir, 'url': reverse('cloud:url', args=("/".join(dirs[:index + 1]),))})
		return urls

	def get_directory(self):
		directory = self.kwargs.get('directory', "")
		return directory

	def get_s3_data(self, directory):
		data = self.storage.listdir(directory)
		folder = data[0]
		files = data[1]
		files = list(filter(lambda x: x['Key'] != '.', files))
		return {'folder': folder, 'files': files}

	def get(self, request, *args, **kwargs):
		if request.GET.get('download'):
			url = self.storage.url(self.get_directory())
			return HttpResponseRedirect(url)
		response = super().get(request, *args, **kwargs)
		return response

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(self.get_s3_data(self.get_directory()))
		context['navs'] = self.get_nav()
		return context

