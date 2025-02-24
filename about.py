import backend

version = backend.get_version()

# page text
c = {"id":"version","text":backend.get_version()['version']}
# section def
s = {"id":"version","title":"Version"}
# navigation
navitm = [{"caption":"about this", "href":"#"}]
