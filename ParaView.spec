Summary:	Parallel visualization application
Name:		ParaView
Version:	4.0.1
Release:	8
License:	BSD
Group:		Applications/Engineering
URL:		http://www.paraview.org/
Source0:	http://www.paraview.org/files/v4.0/%{name}-v%{version}-source.tgz
# Source0-md5:	6a300744eaf32676a3a7e1b42eb642c7
Source1:	%{name}_22x22.png
Source2:	%{name}.xml
Patch0:		%{name}-vtk-use-system-libs.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-system-Protobuf.patch
Patch3:		%{name}-system-netcdf.patch
Patch4:		disable-broken-tests.patch
Patch5:		protobuf.patch
BuildRequires:	Mesa-libOSMesa-devel
BuildRequires:	QtDesigner-devel
BuildRequires:	QtHelp-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtSql-sqlite3
BuildRequires:	QtUiTools-devel
BuildRequires:	QtXmlPatterns-devel
BuildRequires:	QtWebKit-devel
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
BuildRequires:	netcdf-devel
BuildRequires:	netcdf-cxx-devel
BuildRequires:	openssl-devel
BuildRequires:	protobuf-devel
BuildRequires:	python-devel
BuildRequires:	qt4-build
BuildRequires:	readline-devel
BuildRequires:	tk-devel
BuildRequires:	wget
BuildRequires:	zlib-devel
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
Requires:	QtSql-sqlite3
%requires_eq_to	hdf5 hdf5-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	lib.*Python.*\.so.*

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

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-v%{version}-source
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1
#Remove included thirdparty sources just to be sure
for x in protobuf ; do
	rm -r ThirdParty/$x/vtk$x
done
for x in expat freetype gl2ps hdf5 jpeg libxml2 netcdf oggtheora png sqlite tiff zlib ; do
	rm -r VTK/ThirdParty/$x/vtk$x
done

%{__rm} -r ParaViewCore/ServerImplementation/Default/Testing

%build
rm -rf build
mkdir build
cd build
%cmake .. \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_CXX_COMPILER:FILEPATH=%{__cxx} \
	-DCMAKE_C_COMPILER:FILEPATH=%{__cc} \
	-DPV_INSTALL_INCLUDE_DIR:PATH=include/paraview \
	-DPV_INSTALL_LIBRARY_DIR:PATH=%{_lib}/paraview \
	-DTCL_LIBRARY:PATH=tcl \
	-DTK_LIBRARY:PATH=tk \
	-DPARAVIEW_BUILD_PLUGIN_AdiosReader:BOOL=ON \
	-DPARAVIEW_BUILD_PLUGIN_CoProcessingScriptGenerator:BOOL=ON \
	-DPARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL=ON \
	-DPARAVIEW_BUILD_PLUGIN_ForceTime:BOOL=ON \
	-DPARAVIEW_ENABLE_PYTHON:BOOL=ON \
	-DPARAVIEW_INSTALL_THIRD_PARTY_LIBRARIES:BOOL=OFF \
	-DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \
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
	-DVTK_USE_SYSTEM_LIBPROJ4=OFF \
	-DVTK_USE_SYSTEM_LIBRARIES:BOOL=ON \
	-DVTK_USE_SYSTEM_LIBRARIES=ON \
	-DVTK_USE_SYSTEM_PNG:BOOL=ON \
	-DVTK_USE_SYSTEM_TIFF:BOOL=ON \
	-DVTK_USE_SYSTEM_ZLIB:BOOL=ON \
	-DVTK_CUSTOM_LIBRARY_SUFFIX="" \
	-DVTK_USE_INFOVIS:BOOL=OFF \
	-DVTK_USE_SYSTEM_ICET=OFF \
	-DVTK_USE_SYSTEM_NETCDF=ON \
	-DVTK_USE_SYSTEM_QTTESTING=OFF \
	-DVTK_USE_SYSTEM_XDMF2=OFF \
	-DXDMF_WRAP_PYTHON:BOOL=ON \
	-DBUILD_DOCUMENTATION:BOOL=ON \
	-DBUILD_EXAMPLES:BOOL=ON

# -DVTK_PYTHON_SETUP_ARGS="--prefix=/usr --root=$RPM_BUILD_ROOT" \

%{__make} VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_datadir}/mime/packages}

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/mime/packages

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#Create desktop file
cat > $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=ParaView Viewer
GenericName=Data Viewer
Comment=ParaView allows viewing of large data sets
Type=Application
Terminal=false
Icon=ParaView_22x22
MimeType=application/x-paraview;
Categories=Application;Graphics;
Exec=paraview
EOF

# Move python files by hand for now
%{__mv} $RPM_BUILD_ROOT%{_bindir}/Python/vtk $RPM_BUILD_ROOT%{_libdir}/paraview/site-packages/
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}/Python

# Install vtk*Python.so by hand for now
%{__mv} $RPM_BUILD_ROOT%{_libdir}/paraview/vtk*Python.so $RPM_BUILD_ROOT%{_libdir}/paraview/site-packages/paraview/vtk/
%{__mv} $RPM_BUILD_ROOT%{_libdir}/paraview/site-packages/paraview/vtk/vtkPV*Python.so $RPM_BUILD_ROOT%{_libdir}/paraview/site-packages/paraview/

# Cleanup vtk conflicting binaries
%{__rm} $RPM_BUILD_ROOT%{_bindir}/vtk{EncodeString,HashSource,Parse{Java,OGLExt},ProcessShader,Wrap{Hierarchy,Java,Python,Tcl,TclInit,PythonInit}}

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
%dir %{_libdir}/paraview/
%attr(755,root,root) %{_libdir}/paraview/paraview
%attr(755,root,root) %{_libdir}/paraview/pvbatch
%attr(755,root,root) %{_libdir}/paraview/pvdataserver
%attr(755,root,root) %{_libdir}/paraview/pvpython
%attr(755,root,root) %{_libdir}/paraview/pvrenderserver
%attr(755,root,root) %{_libdir}/paraview/pvserver
%attr(755,root,root) %{_libdir}/paraview/smTestDriver
%attr(755,root,root) %{_libdir}/paraview/lib*.so*
%{_libdir}/paraview/.plugins
%dir %{_libdir}/paraview/site-packages
%{_libdir}/paraview/site-packages/autobahn
%dir %{_libdir}/paraview/site-packages/paraview
%{_libdir}/paraview/site-packages/paraview/pv_compile_complete
%{_libdir}/paraview/site-packages/paraview/*.py*
%attr(755,root,root) %{_libdir}/paraview/site-packages/paraview/*.so
%{_libdir}/paraview/site-packages/paraview/demos
%{_libdir}/paraview/site-packages/paraview/vtk
%{_libdir}/paraview/site-packages/twisted
%dir %{_libdir}/paraview/site-packages/vtk
%{_libdir}/paraview/site-packages/vtk/*.py*
%dir %{_libdir}/paraview/site-packages/vtk/gtk
%{_libdir}/paraview/site-packages/vtk/gtk/*.py*
%dir %{_libdir}/paraview/site-packages/vtk/qt4
%{_libdir}/paraview/site-packages/vtk/qt4/*.py*
%dir %{_libdir}/paraview/site-packages/vtk/test
%{_libdir}/paraview/site-packages/vtk/test/*.py*
%dir %{_libdir}/paraview/site-packages/vtk/tk
%{_libdir}/paraview/site-packages/vtk/tk/*.py*
%dir %{_libdir}/paraview/site-packages/vtk/util
%{_libdir}/paraview/site-packages/vtk/util/*.py*
%dir %{_libdir}/paraview/site-packages/vtk/wx
%{_libdir}/paraview/site-packages/vtk/wx/*.py*
%{_libdir}/paraview/site-packages/zope
%{_libdir}/paraview/www
%{_desktopdir}/ParaView.desktop
%{_pixmapsdir}/ParaView_22x22.png
%{_datadir}/mime/packages/ParaView.xml
%dir %{_datadir}/doc/paraview-4.0
%{_datadir}/doc/paraview-4.0/paraview.qch

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vtkkwProcessXML
%attr(755,root,root) %{_bindir}/vtkWrapClientServer
%{_includedir}/paraview
%{_datadir}/cmake/paraview
