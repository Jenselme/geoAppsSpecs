%global project_owner mapserver
%global project_name mapserver
%global commit 5449a6ad858659f3dfed34886237567b207cb85e
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Name:           mapserver6
Version:        6.4.3
Release:        1.git%{shortcommit}%{?dist}
Summary:        Environment for building spatially-enabled internet applications

Group:          Development/Tools
License:        BSD
URL:            http://www.mapserver.org

Source0:        https://github.com/%{project_owner}/%{project_name}/archive/%{commit}/%{project_name}-%{commit}.tar.gz

Requires:       httpd
Requires:       dejavu-sans-fonts

BuildRequires:  cairo-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  fcgi-devel
BuildRequires:  freetype-devel
BuildRequires:  fribidi-devel
BuildRequires:  gd-devel >= 2.0.16
BuildRequires:  gdal-devel
BuildRequires:  geos-devel
BuildRequires:  giflib-devel
BuildRequires:  httpd-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libxml2-devel
BuildRequires:  libXpm-devel
BuildRequires:  libxslt-devel
BuildRequires:  mysql-devel
BuildRequires:  pam-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  postgresql-devel
BuildRequires:  proj-devel
BuildRequires:  readline-devel
BuildRequires:  swig
BuildRequires:  zlib-devel


%description
Mapserver is an internet mapping program that converts GIS data to
map images in real time. With appropriate interface pages,
Mapserver can provide an interactive internet map based on
custom GIS data.


%package  libs
Summary:  %{summary}

%description libs
This package contains the libs for mapserver.


%package  devel
Summary:        Development files for mapserver
Conflicts:      mapserver-devel
Requires:       %{name}

%description devel
This package contains development files for mapserver.

%prep
%setup -q -n mapserver-%{commit}


%build
mkdir build
cd build

export CFLAGS="${CFLAGS} -ldl -fPIC -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -fno-strict-aliasing"

cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_SKIP_RPATH=ON \
      -DCMAKE_C_FLAGS_RELEASE="%{optflags} -fno-strict-aliasing" \
      -DCMAKE_CXX_FLAGS_RELEASE="%{optflags} -fno-strict-aliasing" \
      -DCMAKE_VERBOSE_MAKEFILE=ON \
      -DCMAKE_BUILD_TYPE="Release" \
      -DCMAKE_SKIP_INSTALL_RPATH=ON \
      -DCMAKE_SKIP_RPATH=ON \
      -DWITH_CAIRO=TRUE \
      -DWITH_CLIENT_WFS=TRUE \
      -DWITH_CLIENT_WMS=TRUE \
      -DWITH_CURL=TRUE \
      -DWITH_FCGI=TRUE \
      -DWITH_FRIBIDI=TRUE \
      -DWITH_GD=TRUE \
      -DWITH_GDAL=TRUE \
      -DWITH_GEOS=TRUE \
      -DWITH_GIF=TRUE \
      -DWITH_ICONV=TRUE \
      -DWITH_JAVA=FALSE \
      -DWITH_KML=TRUE \
      -DWITH_LIBXML2=TRUE \
      -DWITH_OGR=TRUE \
      -DWITH_MYSQL=TRUE \
      -DWITH_PERL=FALSE \
      -DCUSTOM_PERL_SITE_ARCH_DIR="%{perl_vendorarch}" \
      -DWITH_PHP=FALSE \
      -DWITH_POSTGIS=TRUE \
      -DWITH_PROJ=TRUE \
      -DWITH_PYTHON=FALSE \
      -DWITH_RUBY=FALSE \
      -DWITH_SOS=TRUE \
      -DWITH_THREAD_SAFETY=TRUE \
      -DWITH_WCS=TRUE \
      -DWITH_WMS=TRUE \
      -DWITH_WFS=TRUE \
      -DWITH_XMLMAPFILE=TRUE \
      -DWITH_POINT_Z_M=TRUE \
      -DWITH_APACHE_MODULE=FALSE \
      -DWITH_SVGCAIRO=FALSE \
      -DWITH_MYSQL=FALSE \
      -DWITH_CSHARP=FALSE \
      -DWITH_ORACLESPATIAL=FALSE \
      -DWITH_ORACLE_PLUGIN=FALSE \
      -DWITH_MSSQL2008=FALSE \
      -DWITH_SDE=FALSE \
      -DWITH_SDE_PLUGIN=FALSE \
      -DWITH_EXEMPI=FALSE \
      ..


make  %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_includedir}/%{name}/

install -p -m 644 xmlmapfile/mapfile.xsd %{buildroot}%{_datadir}/%{name}
install -p -m 644 xmlmapfile/mapfile.xsl %{buildroot}%{_datadir}/%{name}

# install header
install -p -m 644 *.h %{buildroot}%{_includedir}/%{name}/

cd build
make DESTDIR=%{buildroot} install %{?_smp_mflags}

# Rename executables to work with mapserver7
executables=( legend mapserv msencrypt scalebar shp2img shptree shptreetst shptreevis sortshp tile4ms )
for executable in ${executables[@]}; do
    mv "%{buildroot}%{_bindir}/${executable}" "%{buildroot}%{_bindir}/${executable}6"
done


%post libs -p /sbin/ldconfig
%post devel -p  /sbin/ldconfig

%postun libs -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig


%files
%doc README
%{_bindir}/legend6
%{_bindir}/mapserv6
%{_bindir}/msencrypt6
%{_bindir}/scalebar6
%{_bindir}/shp2img6
%{_bindir}/shptree6
%{_bindir}/shptreetst6
%{_bindir}/shptreevis6
%{_bindir}/sortshp6
%{_bindir}/tile4ms6
%{_datadir}/%{name}/

%files libs
%doc README
%{_libdir}/libmapserver.so.%{version}
%{_libdir}/libmapserver.so.1

%files devel
%{_libdir}/libmapserver.so
%{_includedir}/%{name}/


%changelog
* Thu Mar 10 2016 Julien Enselme <jujens@jujens.eu> - 6.4.3-1.git5449a6a
- Update to 6.4.3
- Build it so it can be installed alongside mapserver 7
- Remove all mapscript packages to avoid managing conflits

* Fri Oct 9 2015 Julien Enselme <jujens@jujens.eu> - 6.4.2-1
- Update to 6.4.2

* Fri May 22 2015 Julien Enselme <jujens@jujens.eu> - 6.4.1-1
- Update to 6.4.1
- Switch to CMake
- Disable Ruby and Java
- Patch for php5.6 was merge upstream
- Remove patches for configure file

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.2.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 11 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 6.2.2-2
- Rebuilt for Proj 4.9.1
- Add patch for GCC5 build, also add -fPIC to CFLAGS
- Add a patch for swig 3.0.5

* Tue Dec 23 2014 Pavel Lisý <pali@fedoraproject.org> - 6.2.2-1
- Update to latest 6.2 release
- BZ 1048689 - CVE-2013-7262 mapserver: SQL injections with postgis TIME filters
- BZ 747409 - MapServer uses internal AGG and does not depend on agg-devel

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.2.1-10
- Perl 5.20 rebuild
- Regenerated the wrapper to work with new Perl

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Mat Booth <mat.booth@redhat.com> - 6.2.1-8
- Drop dep on gcj.

* Fri Jun 20 2014 Remi Collet <rcollet@redhat.com> - 6.2.1-7
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file
- add minimal PHP extension load test
- add upstream patch for PHP 5.6 (fix #1111478)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 27 2013 Orion Poplawski <orion@cora.nwra.com> - 6.2.1-5
- Rebuild for gdal 1.10.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 6.2.1-3
- Perl 5.18 rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 6.2.1-2
- rebuild for new GD 2.1.0

* Tue May 21 2013 Pavel Lisý <pali@fedoraproject.org> - 6.2.1-1
- Update to latest stable release
- BZ 910689 - dependency on bitstream-vera-sans-fonts changed to dejavu-sans-fonts
- BZ 960856 - Missing dependency: bitstream-vera-sans-fonts
- BZ 747421 - Move CGI executable from /usr/sbin to /usr/libexec
- BZ 796344 - Not compatible with JDK7
- BZ 846543 - mapserver-java is incorrectly packaged (missing required native library)
- trim of changelog

* Tue Apr 09 2013 Pavel Lisý <pali@fedoraproject.org> - 6.2.0-2
- changed MS_REL from 6x to 62

* Thu Apr 04 2013 Pavel Lisý <pali@fedoraproject.org> - 6.2.0-1
- Update to latest stable release
- dependency on bitstream-vera-sans-fonts replaced to dejavu-sans-fonts

* Mon Mar 25 2013 Oliver Falk <oliver@linux-kernel.at> - 6.0.3-10.1
- Rebuild - fix changelog (bogus date)

* Sat Mar 23 2013 Remi Collet <rcollet@redhat.com> - 6.0.3-10
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 6.0.3-8
- rebuild due to "jpeg8-ABI" feature drop

* Fri Oct 26 2012 Remi Collet <remi@fedoraproject.org> - 6.0.3-7
- conform to PHP Guidelines (#828161)
- add minimal load test for php extension

* Tue Oct 16 2012 Pavel Lisý <pali@fedoraproject.org> - 6.0.3-6
- temporary removed mapserver-java (mapscript) due to build problem
  with jdk7

* Fri Oct 12 2012 Pavel Lisý <pali@fedoraproject.org> - 6.0.3-5
- Merged from 6.0.3-4
- fix of build for php4 and swig > 2.0.4

* Tue Aug 14 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 6.0.3-4
- Rebuilt for new perl.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 6.0.3-2
- Perl 5.16 rebuild

* Sat Jun 30 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 6.0.3-1
- Update to 6.0.3, for various fixes described at:
  https://github.com/mapserver/mapserver/blob/rel-6-0-3-0/HISTORY.TXT
- Update URL, per bz #835426

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 6.0.2-2
- Perl 5.16 rebuild

* Mon Apr 16 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 6.0.2-1
- Update to 6.0.2, for various fixes described at:
  http://trac.osgeo.org/mapserver/browser/tags/rel-6-0-2/mapserver/HISTORY.TXT

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 6.0.1-4
- Rebuild for new libpng

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.0.1-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 6.0.1-2
- Perl mass rebuild

* Mon Jul 18 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 6.0.1-1
- Update to 6.0.1, for various fixes described at:
  http://trac.osgeo.org/mapserver/browser/tags/rel-6-0-1/mapserver/HISTORY.TXT
- Fixes bz #722545
- Apply changes to spec file for new major version.
