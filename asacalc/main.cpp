#include <iostream>

#include <chemkit/molecule.h>
#include <chemkit/moleculefile.h>
#include <chemkit/molecularsurface.h>

using namespace chemkit;
using namespace std;

int main(int argc, char *argv[])
{
	if (argc != 2) {
		std::cerr << "need exactly 1 argument - molecule file name" << endl;
		std::cout << -1;
		return 1;
	}

    chemkit::MoleculeFile file(argv[1]);
    bool ok = file.read();
    if(!ok){
        std::cerr << "Failed to read file" << std::endl;
		std::cout << -1;
        return -1;
    }

    const boost::shared_ptr<chemkit::Molecule> molecule = file.molecule();
    chemkit::MolecularSurface surface(molecule.get());

    // solvent accessible surface
    surface.setSurfaceType(chemkit::MolecularSurface::SolventAccessible);

    //QCOMPARE(qRound(surface.volume()), 443);

	std::cout << surface.surfaceArea();
	return 0;
}
