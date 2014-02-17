Summary:	Parallel visualization application
Name:		ParaView
Version:	3.12.0
Release:	3
License:	BSD
Group:		Applications/Engineering
URL:		http://www.paraview.org/
Source0:	http://www.paraview.org/files/v3.12/%{name}-%{version}.tar.gz
# Source0-md5:	8feabc6261e2060648eaac593d85b1de
Source1:	%{name}_22x22.png
Source2:	%{name}.xml
Patch0:		%{name}-3.8.0-include.patch
Patch1:		%{name}-3.12.0-boost-1.48.0-bfs.patch
Patch2:		%{name}-gcc47.patch
Patch3:		%{name}-3.2.2-hdf5.patch
Patch4:		%{name}-freetype.patch
BuildRequires:	Mesa-libOSMesa-devel
BuildRequires:	QtDesigner-devel
BuildRequires:	QtHelp-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtSql-sqlite
BuildRequires:	QtUiTools-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	freetype-devel
BuildRequires:	gnuplot
BuildRequires:	graphviz
BuildRequires:	hdf5-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtheora-devel
BuildRequires:	libtiff-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	qt4-build
BuildRequires:	readline-devel
BuildRequires:	tk-devel
BuildRequires:	wget
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zlib-devel
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
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

%package        devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
#Remove included hdf5 just to be sure
rm -r VTK/Utilities/vtkhdf5
%patch4 -p0

%build
mkdir build
cd build
%cmake .. \
	-DPV_INSTALL_INCLUDE_DIR:PATH=include/paraview \
	-DPV_INSTALL_LIB_DIR:PATH=%{_lib}/paraview \
	-DTCL_LIBRARY:PATH=tcl \
	-DTK_LIBRARY:PATH=tk \
	-DPARAVIEW_BUILD_PLUGIN_AdiosReader:BOOL=ON \
	-DPARAVIEW_BUILD_PLUGIN_CoProcessingScriptGenerator:BOOL=ON \
	-DPARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL=ON \
	-DPARAVIEW_BUILD_PLUGIN_ForceTime:BOOL=ON \
	-DPARAVIEW_ENABLE_PYTHON:BOOL=ON \
	-DPARAVIEW_INSTALL_THIRD_PARTY_LIBRARIES:BOOL=OFF \
	-DPARAVIEW_INSTALL_DEVELOPMENT:BOOL=ON \
	-DVTK_OPENGL_HAS_OSMESA:BOOL=ON \
	-DVTK_USE_BOOST:BOOL=ON \
	-DVTK_USE_INFOVIS:BOOL=OFF \
	-DVTK_USE_N_WAY_ARRAYS:BOOL=ON \
	-DVTK_USE_OGGTHEORA_ENCODER:BOOL=ON \
	-DVTK_USE_SYSTEM_EXPAT:BOOL=ON \
	-DVTK_USE_SYSTEM_FREETYPE:BOOL=ON \
	-DVTK_USE_SYSTEM_HDF5:BOOL=ON \
	-DVTK_USE_SYSTEM_JPEG:BOOL=ON \
	-DVTK_USE_SYSTEM_PNG:BOOL=ON \
	-DVTK_USE_SYSTEM_TIFF:BOOL=ON \
	-DVTK_USE_SYSTEM_ZLIB:BOOL=ON \
	-DXDMF_WRAP_PYTHON:BOOL=ON \
	-DBUILD_DOCUMENTATION:BOOL=ON \
	-DBUILD_EXAMPLES:BOOL=ON

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

# Install vtk*Python.so by hand for now
cp -p bin/vtk*Python.so $RPM_BUILD_ROOT%{_libdir}/paraview/site-packages/paraview/vtk/
mv $RPM_BUILD_ROOT%{_libdir}/paraview/site-packages/paraview/vtk/vtkPV*Python.so $RPM_BUILD_ROOT%{_libdir}/paraview/site-packages/paraview/

# Cleanup vtk binaries
rm $RPM_BUILD_ROOT%{_bindir}/vtk*

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
%attr(755,root,root) %{_bindir}/pvblot
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
%{_libdir}/paraview/CMake
%{_libdir}/paraview/*.cmake
%{_libdir}/paraview/doc
%{_libdir}/paraview/*.py
%{_libdir}/paraview/testing
%{_libdir}/paraview/.plugins
%{_libdir}/paraview/SESAMEConversions.xml
%{_libdir}/paraview/hints
%{_libdir}/paraview/ParaViewCore
%dir %{_libdir}/paraview/site-packages
%dir %{_libdir}/paraview/site-packages/paraview
%{_libdir}/paraview/site-packages/paraview/pv_compile_complete
%{_libdir}/paraview/site-packages/paraview/*.py*
%attr(755,root,root) %{_libdir}/paraview/site-packages/paraview/*.so
%{_libdir}/paraview/site-packages/paraview/demos
%{_libdir}/paraview/site-packages/paraview/vtk
%{_desktopdir}/ParaView.desktop
%{_pixmapsdir}/ParaView_22x22.png
%{_datadir}/mime/packages/ParaView.xml
%dir %{_datadir}/doc/paraview-3.12
%{_datadir}/doc/paraview-3.12/paraview.qch

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kwProcessXML
%{_includedir}/paraview/
