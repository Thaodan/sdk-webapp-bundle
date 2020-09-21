
Name:           sdk-webapp-bundle
Summary:        Bundle of gems used by sdk-webapp
Version:        0.6.0+sdk
Release:        1
Group:          Development/Languages/Ruby
License:        GPLv2+ or Ruby (see gems)
# This is the BR for all enclosed gems
BuildRequires:  rubygem-bundler gcc-c++ openssl-devel pkgconfig ruby
Requires:       rubygem-bundler
URL:            https://wiki.merproject.org/wiki/Platform_SDK
Source0:        %{name}-%{version}.tar.bz2
Source99:       sdk-webapp-bundle.rpmlintrc
Summary:        Gems needed to run sdk-webapp
%description

This package is the bundle of gems needed to run the Mer SDK webapp.

%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p vendor/cache
cp -a gems/*.gem vendor/cache

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/%{name}
bundle install --local --standalone --deployment --binstubs=%{buildroot}/%{_bindir}/ --no-cache --shebang=%{_bindir}/ruby

cp -a Gemfile Gemfile.lock %{buildroot}/usr/lib/%{name}/
cp -a .bundle %{buildroot}/usr/lib/%{name}/
cp -a vendor %{buildroot}/usr/lib/%{name}/

# Change #!/usr/local/bin/ruby to #!/usr/bin/ruby
fgrep -rl "usr/local/bin" %{buildroot} | xargs --no-run-if-empty sed -i -e 's_/usr/local/bin_/%{_bindir}_'g

# Change ../../../../../BUILD/%{name}-%{version} to {%_libdir}/%{name}
fgrep -rl "../../../../../BUILD/%{name}-%{version}" %{buildroot} | xargs --no-run-if-empty sed -i -e 's_../../../../../BUILD/%{name}-%{version}_%{_libdir}/%{name}_'g

# Remove references to buildroot
fgrep -rl "%{buildroot}" %{buildroot} | xargs --no-run-if-empty sed -i -e 's_%{buildroot}__'g

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}/
%{_bindir}
