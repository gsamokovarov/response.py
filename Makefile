clean:
	@find -name '*.py?' -or -name '.*.sw?' | xargs rm -f

test:
	@python test.py

watch:
	@guard start -c
