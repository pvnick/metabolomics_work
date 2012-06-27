#include <iostream>

#include <chemkit/molecule.h>
#include <chemkit/moleculefile.h>
#include <chemkit/molecularsurface.h>

using namespace chemkit;
using namespace std;

int main(int argc, char *argv[])
{
	if (argc != 3) {
		std::cerr << "need exactly 2 arguments - molecule file name, followed by property name" << endl;
		std::cout << "null";
		return 1;
	}

	char *moleculeFileName = argv[1];
	char *propertyName = argv[2];

    chemkit::MoleculeFile file(moleculeFileName);
    bool ok = file.read();
    if(!ok){
        std::cerr << "Failed to read file" << std::endl;
		std::cout << "null";
        return 1;
    }

    const boost::shared_ptr<chemkit::Molecule> molecule = file.molecule();
	Molecule *moleculePtr = molecule.get();
	Variant propValue = moleculePtr->data(propertyName);
	if (propValue.isNull()) {
		cout << "null";
	} else {
		cout << propValue.toDouble();
	}

	return 0;
}
