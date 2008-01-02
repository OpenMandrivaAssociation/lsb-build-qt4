%define qtver	 4.1.0
%define lsbbuild lsb-build-base

Summary:	LSB Build environment qt package
Name:		lsb-build-qt4
Version:	3.1.1
Release:	%mkrel 1
License:	LGPL
Group:		Development/C++
Source:		ftp://ftp.freestandards.org/pub/lsb/lsbdev/released-3.1.0/source/lsb-build-qt4-%{version}.tar.bz2
Source1:	ftp://ftp.trolltech.com/qt/source/qt-x11-opensource-src-%qtver.tar.bz2
URL:            http://www.linuxbase.org/build
BuildRoot: 	%_tmppath/%name-%version-%release-root
#AutoReqProv:	no
BuildRequires:	chrpath

%description
This package provides LSB qt building support for the
lsb-build packages.

%package        -n %{name}-devel
Summary:        LSB Build environment qt headers
Group:          Development/C++
Requires:	lsb-build-base lsb-build-desktop-devel 
Requires:	lsb-build-c++-devel lsb-build-qt3

%description -n %{name}-devel
This package provides LSB qt building support for the
lsb-build packages.  It adds LSB qt headers.

%prep
%setup -q
tar xjf %{SOURCE1}
# copy the linux-lsb makespec needed for bootstrapping
cp -rpf linux-lsb qt-x11-opensource-src-%qtver/mkspecs

%build
cd qt-x11-opensource-src-%qtver
./configure --prefix=%{_prefix} -headerdir %{_includedir}/%{lsbbuild}/qt4 -libdir %{_libdir}/%{lsbbuild}/qt4 -release -confirm-license
IMAGE=$(pwd)/image
cd src/
for x in corelib gui network opengl sql svg xml; do 
	if [ ! -e "$x/Makefile.Release" ]; then
            echo "No such file: $x/Makefile.Release"
            exit 1
        fi
	cd $x
	# strip dependencies from target headers so we can install them without building anything
        sed -e 's/^install_targ_headers:.*/install_targ_headers:/' Makefile.Release >Makefile.lsb
	make -f Makefile.lsb install_targ_headers INSTALL_ROOT="$IMAGE"
	cd ../
done

# build the moc, rcc, and uic tools
	
cd tools
for i in moc rcc uic; do
	make -C $i
done

%install
rm -rf $RPM_BUILD_ROOT

# install the qmake tool
cd qt-x11-opensource-src-%qtver
mkdir -p $RPM_BUILD_ROOT%{_bindir}
#make install_mkspecs INSTALL_ROOT=$RPM_BUILD_ROOT%{_libdir}/%{lsbbuild}/qt4/

# install the moc, rcc, and uic tools
cp bin/qmake $RPM_BUILD_ROOT%{_bindir}/qmake_lsb_qt4
cp bin/moc $RPM_BUILD_ROOT%{_bindir}/moc_lsb_qt4
cp bin/uic $RPM_BUILD_ROOT%{_bindir}/uic_lsb_qt4
cp bin/rcc $RPM_BUILD_ROOT%{_bindir}
chrpath -d $RPM_BUILD_ROOT/%{_bindir}/*

cd ..
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{lsbbuild}/qt4
cp -rLpf qt-x11-opensource-src-%qtver/image%{_includedir}/%{lsbbuild}/qt4/Qt{Core,Gui,Network,OpenGL,S{ql,vg},Xml} $RPM_BUILD_ROOT%{_includedir}/%{lsbbuild}/qt4

#copy linux-lsb mkspecs
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{lsbbuild}/qt4/mkspecs
cp -rpf linux-lsb $RPM_BUILD_ROOT%{_libdir}/%{lsbbuild}/qt4/mkspecs
cp -rpf qt-x11-opensource-src-%{qtver}/mkspecs/features $RPM_BUILD_ROOT%{_libdir}/%{lsbbuild}/qt4/mkspecs
cp qt-x11-opensource-src-%{qtver}/mkspecs/qconfig.pri $RPM_BUILD_ROOT%{_libdir}/%{lsbbuild}/qt4/mkspecs

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{name}-devel
%defattr(-,root,root)
%doc README Licence GPL
%{_bindir}/qmake_lsb_qt4
%{_bindir}/moc_lsb_qt4
%{_bindir}/uic_lsb_qt4
%{_bindir}/rcc
%{_includedir}/%{lsbbuild}/qt4
%{_libdir}/%{lsbbuild}/qt4/mkspecs

