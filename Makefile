
docs:
	make html_note
	

html_update:
	cp -r ./temp/_build/html/ ./docs/

html_note:
	rm -r ./docs/*.ipynb
	cp -r *.ipynb ./docs

clean_doc:
	rm -r ./docs
	mkdir -p docs