# Location of the Python header files
PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)
# Location of the Boost Python include files and library
BOOST_INC = /usr/include
BOOST_LIB = /usr/lib
BOOST_PY_VERSION = py27
# Compile mesh classes
TARGET = hola

$(TARGET).so: $(TARGET).o
	g++ -shared -Wl,--export-dynamic $(TARGET).o \
            -L$(BOOST_LIB) \
            -lboost_python-$(BOOST_PY_VERSION) \
            -L/usr/lib/python$(PYTHON_VERSION)/config \
            -lpython$(PYTHON_VERSION) -o $(TARGET).so

$(TARGET).o: $(TARGET).C
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).C

clean:
	rm -rf *.o $(TARGET).so *.pyc
