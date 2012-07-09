cmake_minimum_required(VERSION 2.6)

#find qt
find_package(Qt4 4.6 COMPONENTS QtCore QtNetwork QtXml REQUIRED)
set(QT_DONT_USE_QTGUI TRUE)
set(QT_USE_QTNETWORK TRUE)
set(QT_USE_QTXML TRUE)
include(${QT_USE_FILE})

#find boost
find_package(Boost COMPONENTS iostreams system filesystem thread REQUIRED)
link_directories(${Boost_LIBRARY_DIRS})
include_directories(${Boost_INCLUDE_DIRS})

#find chemkit
find_package(Chemkit COMPONENTS io web REQUIRED)
include_directories(${CHEMKIT_INCLUDE_DIRS})

add_executable(get_molecule_property main.cpp)
target_link_libraries(get_molecule_property ${CHEMKIT_IO_LIBRARY} ${CHEMKIT_WEB_LIBRARY} ${CHEMKIT_LIBRARIES} ${QT_LIBRARIES} ${Boost_LIBRARIES})
