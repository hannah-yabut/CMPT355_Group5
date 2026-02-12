# Makefile for AB Puzzle Solver

TARGET := AB
MAIN   := AB.py
MODULES := moves.py

.PHONY: all clean lint

all: $(TARGET)


$(TARGET): $(MAIN) $(MODULES)
	cp $(MAIN) $(TARGET)
	chmod +x $(TARGET)

lint:
	python3 -m py_compile $(MAIN) $(MODULES)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm AB

tar:
	tar -czf ../cmpt355_group5_project1.zip AB.py Makefile moves.py readme.txt