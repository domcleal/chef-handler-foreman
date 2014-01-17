%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name chef_handler_foreman


%define rubyabi 1.8

Summary: Chef handlers to integrate with foreman
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.4
Release: 1%{?dist}
Group: Development/Libraries
License: GPLv3+
URL: https://github.com/theforeman/chef_handler_foreman
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
%if 0%{?rhel} == 6 || 0%{?fedora} < 19
Requires: %{?scl_prefix}ruby(abi) >= %{rubyabi}
%endif
Requires: %{?scl_prefix}rubygems

%if 0%{?rhel} == 6 && 0%{?scl_prefix:0} || 0%{?fedora} > 17
BuildRequires: %{?scl_prefix}rubygems-devel
%else
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_libdir %{gem_dir}/gems/%{gem_name}-%{version}/lib
%endif

%if 0%{?rhel} == 6 || 0%{?fedora} < 19
BuildRequires: %{?scl_prefix}ruby(abi) >= %{rubyabi}
%endif
BuildRequires: %{?scl_prefix}rubygems
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
This gem adds chef handlers so your chef-client can upload attributes (facts) and reports to Foreman

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0} --no-rdoc --no-ri
%{?scl:"}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_instdir}/lib

%doc %{gem_instdir}/LICENSE.txt

%exclude %{gem_instdir}/README.md
%exclude %{gem_cache}
%exclude %{gem_instdir}/Rakefile
# add once tests are added (maybe spec dir instead)
#%exclude %{gem_instdir}/test
%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md

%changelog
* Fri Jan 17 2014 Marek Hulan <mhulan@redhat.com> 0.0.4-1
- new package built with tito


