

html_update:
	cp -r ./temp/_build/html/ ./docs/

clean_doc:
	rm -r ./docs
	mkdir -p docs