Summary:	Offline maps viewer for multiple providers
Name:		gmapcatcher
Version:	0.7.5.0
Release:	0.2
License:	GPL
Group:		Applications
URL:		http://code.google.com/p/gmapcatcher/
Source0:	http://gmapcatcher.googlecode.com/files/GMapCatcher-%{version}.tar.gz
# Source0-md5:	f011f0016f8be4898a4efbf32173994f
Patch0:		setup_py-paths.patch
Requires:	python-pygtk-gtk
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GMapCatcher is an offline maps viewer. It downloads tiles
automatically from many providers such as: CloudMade, OpenStreetMap,
Yahoo Maps, Google Map. It displays them using a custom GUI. User can
view the maps while offline. GMapCatcher doesn't depend on
google-map's java scripts so it should work even if google changes
them. It also provides a downloading tool.

%prep
%setup -q -n GMapCatcher-%{version}
%patch0
find gmapcatcher -name "*.py" | xargs %{__sed} -i -e '1s,^#!.*python,#!%{__python},'
gzip man/*

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--prefix=%{_prefix} \
	--root=$RPM_BUILD_ROOT \
	--install-scripts=%{_prefix}/lib/gmapcatcher

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

rm -rf $RPM_BUILD_ROOT%{_docdir}/mapcatcher

install -d $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}

# Remove eronious folders from list of filenames
install -d $RPM_BUILD_ROOT%{_bindir}
ln -s %{_prefix}/lib/gmapcatcher/maps.py $RPM_BUILD_ROOT%{_bindir}/gmapcatcher
ln -s %{_prefix}/lib/gmapcatcher/download.py $RPM_BUILD_ROOT%{_bindir}/gmapcatcher-cli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gmapcatcher
%attr(755,root,root) %{_bindir}/gmapcatcher-cli
%{_mandir}/man1/mapcatcher.1*
%{_mandir}/man1/mapdownloader.1*
%{_desktopdir}/gmapcatcher.desktop
%{_pixmapsdir}/map.png
%{_pixmapsdir}/gmapcatcher
%dir %{_prefix}/lib/gmapcatcher
%attr(755,root,root) %{_prefix}/lib/gmapcatcher/download.py
%attr(755,root,root) %{_prefix}/lib/gmapcatcher/maps.py
%dir %{py_sitescriptdir}/gmapcatcher
%{py_sitescriptdir}/gmapcatcher/*.py[co]
%{py_sitescriptdir}/gmapcatcher/pyGPSD
%{py_sitescriptdir}/gmapcatcher/mapServers
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/GMapCatcher-*.egg-info
%endif
