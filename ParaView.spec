#
# Conditional build:
%bcond_with	system_protobuf		# build with system protobuf library
#
Summary:	Parallel visualization application
Summary(pl.UTF-8):	Aplikacja do równoległej wizualizacji
Name:		ParaView
Version:	5.5.0
Release:	0.1
License:	BSD
Group:		Applications/Engineering
Source0:	http://www.paraview.org/files/v5.5/%{name}-v%{version}.tar.gz
# Source0-md5:	a8f2f41edadffdcc89b37fdc9aa7f005
Source1:	%{name}.xml
Patch0:		link.patch
URL:		http://www.paraview.org/
BuildRequires:	Mesa-libOSMesa-devel
BuildRequires:	Qt5Designer-devel
BuildRequires:	Qt5Help-devel
BuildRequires:	Qt5Sql-devel
BuildRequires:	Qt5Sql-sqldriver-sqlite3
BuildRequires:	Qt5UiTools-devel
BuildRequires:	Qt5WebKit-devel
BuildRequires:	Qt5XmlPatterns-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	freetype-devel
BuildRequires:	gl2ps-devel
BuildRequires:	gnuplot
BuildRequires:	graphviz
BuildRequires:	hdf5-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtheora-devel
BuildRequires:	libtiff-devel
BuildRequires:	netcdf-cxx-devel
BuildRequires:	netcdf-devel
BuildRequires:	openssl-devel
%{?with_system_protobuf:BuildRequires:	protobuf-devel}
BuildRequires:	python-devel
BuildRequires:	qt5-assistant
BuildRequires:	qt5-build
BuildRequires:	readline-devel
BuildRequires:	tk-devel
BuildRequires:	wget
BuildRequires:	zlib-devel
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
Requires:	Qt5Sql-sqldriver-sqlite3
%requires_eq_to	hdf5 hdf5-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	lib.*Python.*\.so.*

# avoid provide clash with vtk.spec
%define		_noautoprov		libvtk.*\.so.* vtk.*\.so.*
%define		_noautoreq		libvtk.*\.so.* vtk.*\.so.*

%description
ParaView is an application designed with the need to visualize large
data sets in mind. The goals of the ParaView project include the
following:

- Develop an open-source, multi-platform visualization application.
- Support distributed computation models to process large data sets.
- Create an open, flexible, and intuitive user interface.
- Develop an extensible architecture based on open standards.

ParaView runs on distributed and shared memory parallel as well as
single processor systems and has been successfully tested on Windows,
Linux and various Unix workstations and clusters. Under the hood,
ParaView uses the Visualization Toolkit as the data processing and
rendering engine and has a user interface written using a unique blend
of Tcl/Tk and C++.

NOTE: The version in this package has NOT been compiled with MPI
support.

%description -l pl.UTF-8
ParaView to aplikacja zaprojektowana z myślą o potrzebie wizualizacji
dużych zbiorów danych. Cele projektu ParaView obejmują:
- rozwijanie mającej otwarte źródła, wieloplatformowej aplikacji do
  wizualizacji
- obsługę rozproszonych modeli obliczeń do przetwarzania dużych
  zbiorów danych
- stworzenie otwartego, elastycznego i intuicyjnego interfejsu
  użytkownika
- rozwijanie rozszerzalnej architektury opartej na otwartych
  standardach

ParaView działa równolegle z rozproszoną i współdzieloną pamięcią, jak
i na systemach z jednym procesorem; został przetestowany na systemach
Windows, Linux, różnych uniksowych stacjach roboczych i klastrach.
Wewnętrznie ParaView wykorzystuje VTK (Visualization Toolkit) jako
silnik przetwarzania danych i renderowania oraz interfejs użytkownika
wykorzystujący unikalne połączenie Tcl/Tk oraz C++.

Uwaga: ta wersja pakietu została skompilowana bez obsługi MPI.

%package devel
Summary:	Development files for ParaView
Summary(pl.UTF-8):	Pliki programistyczne ParaView
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use ParaView.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących ParaView.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1

%if %{with system_protobuf}
#Remove included thirdparty sources just to be sure
%{__rm} -r ThirdParty/protobuf/vtkprotobuf
%endif

for x in expat freetype hdf5 jpeg libxml2 netcdf png sqlite tiff zlib ; do
	%{__rm} -r VTK/ThirdParty/$x/vtk$x
done

%build
rm -rf build
mkdir build
cd build
%cmake .. \
	-DCMAKE_CXX_FLAGS="%{rpmcxxflags} -DNDEBUG -DQT_NO_DEBUG" \
	-DCMAKE_C_FLAGS="%{rpmcflags} -DNDEBUG -DQT_NO_DEBUG" \
	-DCMAKE_Fortran_FLAGS="%{rpmcflags} -DNDEBUG -DQT_NO_DEBUG" \
	-DCMAKE_EXE_LINKER_FLAGS="%{rpmldflags}" \
	-DCMAKE_SHARED_LINKER_FLAGS="%{rpmldflags}" \
	-DCMAKE_MODULE_LINKER_FLAGS="%{rpmldflags}" \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_CXX_COMPILER:FILEPATH=%{__cxx} \
	-DCMAKE_C_COMPILER:FILEPATH=%{__cc} \
	-DPV_INSTALL_INCLUDE_DIR:PATH=include/paraview \
	-DPV_INSTALL_LIBRARY_DIR:PATH=%{_lib}/paraview \
	-DTCL_LIBRARY:PATH=tcl \
	-DTK_LIBRARY:PATH=tk \
	-DPARAVIEW_BUILD_PLUGIN_AdiosReader:BOOL=ON \
	-DPARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL=ON \
	-DPARAVIEW_ENABLE_PYTHON:BOOL=ON \
	-DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \
	-DQT_XMLPATTERNS_EXECUTABLE:FILEPATH=%{_bindir}/xmlpatterns-qt5 \
	-DQT_HELP_GENERATOR:FILEPATH=%{_bindir}/qhelpgenerator-qt5 \
	-DVTK_INSTALL_ARCHIVE_DIR:PATH=%{_lib}/paraview \
	-DVTK_INSTALL_INCLUDE_DIR:PATH=include/paraview \
	-DVTK_INSTALL_LIBRARY_DIR:PATH=%{_lib}/paraview \
	-DVTK_INSTALL_PACKAGE_DIR=share/cmake/paraview \
	-DVTK_USE_BOOST:BOOL=ON \
	-DVTK_USE_INFOVIS:BOOL=OFF \
	-DVTK_USE_N_WAY_ARRAYS:BOOL=ON \
	-DVTK_USE_OGGTHEORA_ENCODER:BOOL=ON \
	-DVTK_USE_SYSTEM_EXPAT:BOOL=ON \
	-DVTK_USE_SYSTEM_FREETYPE:BOOL=ON \
	-DFREETYPE_INCLUDE_DIRS=%{_includedir}/freetype2 \
	-DVTK_USE_SYSTEM_HDF5:BOOL=ON \
	-DVTK_USE_SYSTEM_HDF5=ON \
	-DHDF5_HL_LIBRARY:FILEPATH=%{_libdir}/libhdf5_hl.so \
	-DVTK_USE_SYSTEM_JPEG:BOOL=ON \
	-DVTK_USE_SYSTEM_CGNS:BOOL=OFF \
	-DVTK_USE_SYSTEM_LIBPROJ4:BOOL=OFF \
	-DVTK_USE_SYSTEM_JSONCPP:BOOL=OFF \
	-DVTK_USE_SYSTEM_LIBHARU:BOOL=OFF \
	-DVTK_USE_SYSTEM_LIBRARIES:BOOL=ON \
	-DVTK_USE_SYSTEM_LIBRARIES=ON \
	-DVTK_USE_SYSTEM_PNG:BOOL=ON \
	-DVTK_USE_SYSTEM_PROTOBUF:BOOL=%{?with_system_protobuf:ON}%{!?with_system_protobuf:OFF} \
	-DVTK_USE_SYSTEM_TIFF:BOOL=ON \
	-DVTK_USE_SYSTEM_ZLIB:BOOL=ON \
	-DVTK_CUSTOM_LIBRARY_SUFFIX="" \
	-DVTK_USE_INFOVIS:BOOL=OFF \
	-DVTK_USE_SYSTEM_ICET=OFF \
	-DVTK_USE_SYSTEM_NETCDF=ON \
	-DVTK_USE_SYSTEM_QTTESTING=OFF \
	-DVTK_USE_SYSTEM_XDMF2=OFF \
	-DVTK_USE_SYSTEM_GL2PS:BOOL=OFF \
	-DXDMF_WRAP_PYTHON:BOOL=ON \
	-DBUILD_DOCUMENTATION:BOOL=ON \
	-DBUILD_EXAMPLES:BOOL=ON

# -DVTK_PYTHON_SETUP_ARGS="--prefix=/usr --root=$RPM_BUILD_ROOT" \

%{__make} VERBOSE=1
%{__make} DoxygenDoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/mime/packages

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/mime/packages

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Replace desktop file
cat > $RPM_BUILD_ROOT%{_desktopdir}/paraview.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=ParaView
Comment=Parallel visualization application
Type=Application
Terminal=false
Icon=paraview
MimeType=application/x-paraview;
Categories=Application;Graphics;
Exec=paraview
EOF

# Cleanup vtk conflicting binaries
%{__rm} $RPM_BUILD_ROOT%{_bindir}/vtk{ParseJava,Wrap{Hierarchy,Java,Python,PythonInit}}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/paraview/lib*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database
%update_mime_database

%postun
/sbin/ldconfig
%update_desktop_database
%update_mime_database

%files
%defattr(644,root,root,755)
%doc License_v1.2.txt
%attr(755,root,root) %{_bindir}/paraview
%attr(755,root,root) %{_bindir}/pvbatch
%attr(755,root,root) %{_bindir}/pvdataserver
%attr(755,root,root) %{_bindir}/pvpython
%attr(755,root,root) %{_bindir}/pvrenderserver
%attr(755,root,root) %{_bindir}/pvserver
%attr(755,root,root) %{_bindir}/smTestDriver
%dir %{_libdir}/paraview
%attr(755,root,root) %{_libdir}/paraview/paraview
%attr(755,root,root) %{_libdir}/paraview/pvbatch
%attr(755,root,root) %{_libdir}/paraview/pvdataserver
%attr(755,root,root) %{_libdir}/paraview/pvpython
%attr(755,root,root) %{_libdir}/paraview/pvrenderserver
%attr(755,root,root) %{_libdir}/paraview/pvserver
%attr(755,root,root) %{_libdir}/paraview/smTestDriver
%attr(755,root,root) %{_libdir}/paraview/lib*.so*
%dir %{_libdir}/paraview/paraview-5.5
%dir %{_libdir}/paraview/paraview-5.5/plugins
%{_libdir}/paraview/paraview-5.5/plugins/.plugins
%dir %{_libdir}/paraview/paraview-5.5/plugins/AcceleratedAlgorithms
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/AcceleratedAlgorithms/libAcceleratedAlgorithms.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/AdiosClientOnly
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/AdiosClientOnly/libAdiosClientOnly.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/AnalyzeNIfTIIO
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/AnalyzeNIfTIIO/libAnalyzeNIfTIIO.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/ArrowGlyph
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/ArrowGlyph/libArrowGlyph.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/CDIReader
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/CDIReader/libCDIReader.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/DigitalRockPhysics
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/DigitalRockPhysics/libDigitalRockPhysics.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/EmbossingRepresentations
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/EmbossingRepresentations/libEmbossingRepresentations.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/EyeDomeLightingView
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/EyeDomeLightingView/libEyeDomeLightingView.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/GMVReader
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/GMVReader/libGMVReader.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/GeodesicMeasurement
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/GeodesicMeasurement/libGeodesicMeasurement.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/LagrangianParticleTracker
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/LagrangianParticleTracker/libLagrangianParticleTracker.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/Moments
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/Moments/libMoments.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/NonOrthogonalSource
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/NonOrthogonalSource/libNonOrthogonalSource.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/PacMan
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/PacMan/libPacMan.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/SLACTools
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/SLACTools/libSLACTools.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/SierraPlotTools
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/SierraPlotTools/libSierraPlotTools.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/StreamLinesRepresentation
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/StreamLinesRepresentation/libStreamLinesRepresentation.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/StreamingParticles
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/StreamingParticles/libStreamingParticles.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/SurfaceLIC
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/SurfaceLIC/libSurfaceLIC.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/ThickenLayeredCells
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/ThickenLayeredCells/libThickenLayeredCells.so
%dir %{_libdir}/paraview/paraview-5.5/plugins/VTKmFilters
%attr(755,root,root) %{_libdir}/paraview/paraview-5.5/plugins/VTKmFilters/libVTKmFilters.so
%dir %{_libdir}/paraview/python*
%dir %{_libdir}/paraview/python*/site-packages
%{_libdir}/paraview/python*/site-packages/*.py*
%dir %{_libdir}/paraview/python*/site-packages/cinema_python
%{_libdir}/paraview/python*/site-packages/cinema_python/*.py*
%dir %{_libdir}/paraview/python*/site-packages/cinema_python/adaptors
%{_libdir}/paraview/python*/site-packages/cinema_python/adaptors/*.py*
%dir %{_libdir}/paraview/python*/site-packages/cinema_python/adaptors/paraview
%{_libdir}/paraview/python*/site-packages/cinema_python/adaptors/paraview/*.py*
%dir %{_libdir}/paraview/python*/site-packages/cinema_python/adaptors/vtk
%{_libdir}/paraview/python*/site-packages/cinema_python/adaptors/vtk/*.py*
%dir %{_libdir}/paraview/python*/site-packages/cinema_python/database
%{_libdir}/paraview/python*/site-packages/cinema_python/database/*.py*
%dir %{_libdir}/paraview/python*/site-packages/cinema_python/images
%{_libdir}/paraview/python*/site-packages/cinema_python/images/*.py*
%dir %{_libdir}/paraview/python*/site-packages/paraview
%{_libdir}/paraview/python*/site-packages/paraview/*.py*
%dir %{_libdir}/paraview/python*/site-packages/paraview/benchmark
%{_libdir}/paraview/python*/site-packages/paraview/benchmark/*.py*
%dir %{_libdir}/paraview/python*/site-packages/paraview/demos
%{_libdir}/paraview/python*/site-packages/paraview/demos/*.py*
%dir %{_libdir}/paraview/python*/site-packages/paraview/web
%{_libdir}/paraview/python*/site-packages/paraview/web/*.py*
%dir %{_libdir}/paraview/python*/site-packages/pygments
%{_libdir}/paraview/python*/site-packages/pygments/*.py*
%dir %{_libdir}/paraview/python*/site-packages/pygments/filters
%{_libdir}/paraview/python*/site-packages/pygments/filters/*.py*
%dir %{_libdir}/paraview/python*/site-packages/pygments/formatters
%{_libdir}/paraview/python*/site-packages/pygments/formatters/*.py*
%dir %{_libdir}/paraview/python*/site-packages/pygments/lexers
%{_libdir}/paraview/python*/site-packages/pygments/lexers/*.py*
%dir %{_libdir}/paraview/python*/site-packages/pygments/styles
%{_libdir}/paraview/python*/site-packages/pygments/styles/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules
%{_libdir}/paraview/python*/site-packages/vtkmodules/*.py*
%attr(755,root,root) %{_libdir}/paraview/python*/site-packages/vtkmodules/*.so
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/gtk
%{_libdir}/paraview/python*/site-packages/vtkmodules/gtk/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/numpy_interface
%{_libdir}/paraview/python*/site-packages/vtkmodules/numpy_interface/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/qt
%{_libdir}/paraview/python*/site-packages/vtkmodules/qt/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/qt4
%{_libdir}/paraview/python*/site-packages/vtkmodules/qt4/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/test
%{_libdir}/paraview/python*/site-packages/vtkmodules/test/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/tk
%{_libdir}/paraview/python*/site-packages/vtkmodules/tk/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/util
%{_libdir}/paraview/python*/site-packages/vtkmodules/util/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/web
%{_libdir}/paraview/python*/site-packages/vtkmodules/web/*.py*
%dir %{_libdir}/paraview/python*/site-packages/vtkmodules/wx
%{_libdir}/paraview/python*/site-packages/vtkmodules/wx/*.py*
%{_desktopdir}/paraview.desktop
%{_datadir}/appdata/paraview.appdata.xml
%{_iconsdir}/hicolor/*/apps/paraview.png
%{_datadir}/mime/packages/ParaView.xml
%dir %{_docdir}/paraview-5.5
%{_docdir}/paraview-5.5/doxygen
%{_docdir}/paraview-5.5/verdict
%{_docdir}/paraview-5.5/paraview.qch

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vtkkwProcessXML
%attr(755,root,root) %{_bindir}/vtkWrapClientServer
%attr(755,root,root) %{_bindir}/paraview-config
%attr(755,root,root) %{_bindir}/vtkLegacyColorMapXMLToJSON
%{_includedir}/paraview
%{_datadir}/cmake/paraview
%{_libdir}/paraview/paraview-config
%{_libdir}/paraview/vtkLegacyColorMapXMLToJSON
#%{_prefix}/lib/cmake/qttesting/ParaViewTargets-relwithdebinfo.cmake
#%{_prefix}/lib/cmake/qttesting/ParaViewTargets.cmake
#%{_prefix}/lib/cmake/qttesting/QtTestingConfig.cmake
