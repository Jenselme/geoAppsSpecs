Name:           tinyows
Version:        1.1.1
Release:        1
License:        MIT
Url:         	http://mapserver.org/tinyows/
Source:         https://github.com/mapserver/tinyows/archive/v.%{version}.tar.gz
Summary:        A simple WFS-T server based on PostGIS spatial database

Requires:       postgresql
Requires:		postgis >= 2.0
Requires:       fcgi
Requires:		libxml2 >= 2.7.0
Requires:		flex

BuildRequires: 	pkgconfig
BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:  chrpath
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  postgresql-devel
BuildRequires:  fcgi-devel
BuildRequires:  libxml2-devel
BuildRequires:  xz
BuildRequires:	flex
BuildRequires:	flex-devel
BuildRequires:	postgis >= 2.0
BuildRequires:	git
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	graphviz-gd
BuildRequires:	fdupes
BuildRequires:	hdf5-devel >= 1.8.11


%package doc
Summary: 	Documentation & demos for TinyOWS


%description
TinyOWS was written with the following things in mind:
- KISS approach !
- As OGC standard compliant as possible, aiming to support:
   - WFS (1.0 and 1.1)
   - FE (1.0 and 1.1)
- Performance is a matter, maps are cool as they're quick to display
- Clean source code
TinyOWS is part of the mapserver suite.


%description doc
TinyOWS WFS-T server this package contain doc and demo


%prep
%setup -q -n %{name}-v.%{version}

%build
autoconf

%configure \
 --with-xml2-config=%{_bindir}/xml2-config \
 --with-shp2pgsql=`pg_config --bindir`/shp2pgsql \
 --with-fastcgi=/usr \

make flex

make %{?_smp_mflags} 

# Make doxygen documentation
make doxygen

%install
mkdir -p %{buildroot}/%{_bindir}
install -p -m 755 tinyows %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/%{_datadir}/%{name}/schema
cp -rf schema %{buildroot}/%{_datadir}/%{name}/

# demo config file
%fdupes -s doc/doxygen

%check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license LICENSE
%doc README NEWS 
%{_bindir}/tinyows
%{_datadir}/%{name}/

%files doc
%license LICENSE
%doc doc/doxygen
%doc demo


%changelog
* Fri Oct 9 2015 Julien Enselme <jujens@jujens.eu> - 1.1.1-1
- Initial packaging

