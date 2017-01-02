# Generated from http_parser.rb-0.6.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name http_parser.rb

Name:		rubygem-%{gem_name}
Version:	0.6.0
Release:	2%{?dist}
Summary:	Simple callback-based HTTP request/response parser
Group:		Development/Languages
License:	MIT
URL:		https://github.com/tmm1/http_parser.rb
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fedora ships with RSpec 3.0 and the Expectations have a different
# name. Patch aims to update them to the newer Expectations.
Patch0:		http_parser.rb-0.6.0-rspec3.patch
Patch1:		http_parser.rb-0.6.0-usr_bin_ruby.patch
BuildRequires:  ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	ruby-devel
BuildRequires:	rubygem(rspec)

%if 0%{?fedora} <= 20 || 0%{?el7}
Provides:	rubygem(%{gem_name}) = %{version}
%endif

%description
Ruby bindings to http://github.com/joylent/http-parser and
http://github.com/a2800276/http-parser.java.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%patch0 -p1
%patch1 -p1

gem build %{gem_name}.gemspec

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
%gem_install

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%if 0%{?fedora} > 0
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -ar .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/
%endif

%if 0%{?rhel} >= 7
mkdir -p %{buildroot}%{gem_extdir_mri}/lib
cp -ar .%{gem_instdir}/lib/ruby_http_parser.so %{buildroot}%{gem_extdir_mri}/lib
%endif

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.gitmodules,Gemfile.lock}

# Run the test suite
%check
pushd .%{gem_instdir}
# Workaround for issue https://github.com/tmm1/http_parser.rb/issues/27
export LC_ALL=en_US.UTF-8
rspec -Ilib -I%{buildroot}%{gem_extdir_mri} spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_extdir_mri}/gem.build_complete
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.md
%license %{gem_instdir}/LICENSE-MIT
%doc %{gem_instdir}/Gemfile

%files doc
%doc %{gem_docdir}
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%{gem_instdir}/bench
%{gem_instdir}/tasks

%changelog
* Fri Sep 02 2016 Yanis Guenane <yguenane@redhat.com> - 0.6.0-2
- Patch the spec file to match key words in RSpec 3
* Mon Jan 05 2015 Graeme Gillies <ggillies@redhat.com> - 0.6.0-1
- Initial package
