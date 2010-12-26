Summary:	Offline maps viewer for multiple providers
Name:		gmapcatcher
Version:	0.7.5.0
Release:	1
License:	GPL
Group:		Applications
URL:		http://code.google.com/p/gmapcatcher/
Source0:	http://gmapcatcher.googlecode.com/files/GMapCatcher-%{version}.tar.gz
# Source0-md5:	f011f0016f8be4898a4efbf32173994f
Patch0:		setup_py-paths.patch
Requires:	python-modules-sqlite
Requires:	python-pygtk-gtk
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GMapCatcher is an offline maps viewer. It downloads tiles
automatically from many providers such as: CloudMade, OpenStreetMap,
Yahoo Maps, Google Map. It displays them using a custom GUI. User can
view the maps while offline. GMapCatcher doesn't depend on
google-map's javascripts so it should work even if google changes
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
	--install-scripts=%{_bindir}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

rm -rf $RPM_BUILD_ROOT%{_docdir}/mapcatcher

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_bindir}}
cp -a %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}
sed -i -e 's,Exec=mapcatcher,Exec=%{name},' $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
sed -i -e 's,Icon=mapcatcher,Icon=%{name},' $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

mv $RPM_BUILD_ROOT%{_pixmapsdir}/{map,%{name}}.png
mv $RPM_BUILD_ROOT%{_bindir}/{maps.py,%{name}}
mv $RPM_BUILD_ROOT%{_bindir}/{download.py,%{name}downloader}
mv $RPM_BUILD_ROOT%{_mandir}/man1/{mapcatcher.1,%{name}.1}.gz
mv $RPM_BUILD_ROOT%{_mandir}/man1/{mapdownloader.1,%{name}downloader.1}.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}downloader
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}downloader.1*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_pixmapsdir}/%{name}
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%{py_sitescriptdir}/%{name}/pyGPSD
%{py_sitescriptdir}/%{name}/mapServers
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/GMapCatcher-*.egg-info
%endif
