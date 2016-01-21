%{?scl:%scl_package %{vagrant_plugin_name}}
%{!?scl:%global pkg_name %{name}}

%global vagrant_plugin_name vagrant-libvirt

Name: %{?scl_prefix}%{vagrant_plugin_name}
Version: 0.0.32
Release: 1%{?dist}
Summary: libvirt provider for Vagrant
Group: Development/Languages
License: MIT
URL: https://github.com/pradels/vagrant-libvirt
Source0: https://rubygems.org/gems/%{vagrant_plugin_name}-%{version}.gem
Source1: 10-vagrant-libvirt.rules
Requires(pre): shadow-utils
Requires(posttrans): %{?scl_prefix}vagrant
Requires(preun): %{?scl_prefix}vagrant

Requires: %{?scl_prefix}rubygem(fog-libvirt)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(nokogiri) => 1.6.0
Requires: %{?scl_prefix}rubygem(nokogiri) < 1.7
Requires: %{?scl_prefix_ror}rubygem(multi_json)
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: polkit
Requires: %{?scl_prefix}vagrant
BuildRequires: %{?scl_prefix}vagrant
BuildRequires: %{?scl_prefix_ror}rubygem(rspec) < 3
BuildRequires: %{?scl_prefix}rubygem(fog-libvirt)
BuildArch: noarch

Provides: %{?scl_prefix}vagrant(%{vagrant_plugin_name}) = %{version}

%description
libvirt provider for Vagrant.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{vagrant_plugin_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{vagrant_plugin_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{vagrant_plugin_name}.gemspec
%{?scl:EOF}
%vagrant_plugin_install

%install
mkdir -p %{buildroot}%{vagrant_plugin_dir}
cp -a .%{vagrant_plugin_dir}/* \
        %{buildroot}%{vagrant_plugin_dir}/

# polkit rule for vagrant group.
#mkdir -p %{buildroot}%{_datadir}/polkit-1/rules.d
#install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/polkit-1/rules.d/

# polkit example as doc
mkdir -p %{buildroot}%{vagrant_plugin_docdir}/polkit
install -m 0644 %{SOURCE1} %{buildroot}%{vagrant_plugin_docdir}/polkit

%check
#pushd .%{vagrant_plugin_instdir}
#sed -i '/:git/ s|:git.*$|:path => "%{vagrant_dir}"|' Gemfile
#sed -i '/rspec/ s|\[\".*\"]|["~> 2.0"]|' vagrant-libvirt.gemspec

#bundle exec rspec spec
#popd

%pre
getent group vagrant >/dev/null || groupadd -r vagrant

%posttrans
%{?scl:env -i - scl enable %{scl} - << \EOF}
%vagrant_plugin_register %{vagrant_plugin_name}
%{?scl:EOF}

%preun
%{?scl:env -i - scl enable %{scl} - << \EOF}
%vagrant_plugin_unregister %{vagrant_plugin_name}
%{?scl:EOF}

%files
%dir %{vagrant_plugin_instdir}
%{vagrant_plugin_libdir}
%{vagrant_plugin_instdir}/locales
%{vagrant_plugin_instdir}/tools
%exclude %{vagrant_plugin_cache}
%exclude %{vagrant_plugin_instdir}/.*
%{vagrant_plugin_spec}
# TODO: Disabled for now, since this might have security implications.
#%%exclude %%{_datadir}/polkit-1/rules.d/10-vagrant.rules
%doc %{vagrant_plugin_instdir}/LICENSE

%files doc
%doc %{vagrant_plugin_docdir}
%doc %{vagrant_plugin_instdir}/example_box
%doc %{vagrant_plugin_instdir}/CHANGELOG.md
%doc %{vagrant_plugin_instdir}/README.md
%{vagrant_plugin_instdir}/Rakefile
%{vagrant_plugin_instdir}/Gemfile
%{vagrant_plugin_instdir}/vagrant-libvirt.gemspec
%{vagrant_plugin_instdir}/spec

%changelog
* Thu Jan 21 2016 Pavel Valena <pvalena@redhat.com> - 0.0.32-1
- Update to 0.0.32
- Remove unnecessary 'runtime' from Requires
- Remove specific version dependency for fog-libvirt
- Add ruby(release) to Requires
- Exclude hidden files
- Remove libvirt from Requires
- Remove qemu-kvm and libvirt-daemon-kvm from Requires
- Remove unnecessary provide
- %%vagrant_plugin_install macro does not need SCL enabled
- Shebang is already removed, no need to remove it

* Tue Jan 05 2016 Pavel Valena <pvalena@redhat.com> - 0.0.30-3
- Clear environment for scriptlets

* Thu Aug 06 2015 Vít Ondruch <vondruch@redhat.com> - 0.0.30-2
- Rebuild to use correct version of scl-utils.
- Resolves: rhbz#1250147

* Fri Jun 12 2015 Josef Stribny <jstribny@redhat.com> - 0.0.30-1
- Update to 0.0.30

* Wed Apr 22 2015 Josef Stribny <jstribny@redhat.com> - 0.0.24-2
- Fix halting

* Thu Feb 19 2015 Josef Stribny <jstribny@redhat.com> - 0.0.24-1
- Update to 0.0.24
- Adjust description
- Rename patch
- Rename policy
- Add virtual provide
- Move license to the main package
- Remove shebang from non-executable Rakefile
- Ship polkit rules as doc

* Wed Jan 07 2015 Josef Stribny <jstribny@redhat.com> - 0.0.23-12
- Require qemu-kvm on RHEL 6

* Fri Jan 02 2015 Josef Stribny <jstribny@redhat.com> - 0.0.23-11
- Do not require libvirt-daemon-kvm on RHEL 6

* Wed Dec 17 2014 Josef Stribny <jstribny@redhat.com> - 0.0.23-10
- Run plugin installation within scl enable

* Mon Dec 15 2014 Josef Stribny <jstribny@redhat.com> - 0.0.23-9
- Add explicit dep on vagrant1-runtime

* Wed Dec 03 2014 Josef Stribny <jstribny@redhat.com> - 0.0.23-8
- rebuilt

* Wed Dec 03 2014 Josef Stribny <jstribny@redhat.com> - 0.0.23-7
- Change ruby-libvirt dep to rubygem-ruby-libvirt

* Wed Dec 03 2014 Josef Stribny <jstribny@redhat.com> - 0.0.23-6
- Use scl enable block for plugin (un)registration

* Tue Dec 02 2014 Josef Stribny <jstribny@redhat.com> - 0.0.23-5
- Fix SCL requires on Vagrant

* Fri Nov 28 2014 Tomas Hrcka - 0.0.23-4
- SCLize spc
- require ruby-libvirt

* Wed Nov 26 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.23-3
- Enable test suite.
- Update polkit rules.

* Mon Nov 24 2014 Josef Stribny <jstribny@redhat.com> - 0.0.23-2
- Register and unregister the plugin using macros

* Tue Oct 14 2014 Josef Stribny <jstribny@redhat.com> - 0.0.23-1
- Update to 0.0.23
- Use ruby-libvirt 0.5.x
- Move the rest of the doc files to -doc

* Tue Sep 16 2014 Josef Stribny <jstribny@redhat.com> - 0.0.20-2
- Register and unregister automatically

* Wed Sep 10 2014 Josef Stribny <jstribny@redhat.com> - 0.0.20-1
- Update to 0.0.20

* Fri Jun 27 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.0.16-1
- Initial package for Fedora
