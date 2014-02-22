char const* greet(){
    return "Hola, world!";
}

#include <boost/python.hpp>
BOOST_PYTHON_MODULE(hola){
    using namespace boost::python;
    def("greet", greet);
}
