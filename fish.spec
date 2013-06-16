Name:           fish
Version:        2.0.0
Release:        1%{?dist}
Summary:        A Friendly Interactive SHell

License:        GPLv2
Group:          System Environment/Shells
URL:            http://fishshell.com/
Source0:        http://fishshell.com/files/2.0.0/fish-2.0.0.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel gettext groff
BuildRequires:  autoconf chrpath gzip


%description
fish is a shell geared towards interactive use. Its features are
focused on user friendliness and discoverability. The language syntax
is simple but incompatible with other shell languages.

%prep
%setup -q -n fish


%build
autoconf
%configure docdir=%_datadir/doc/%{name}-%{version}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

chrpath --delete $RPM_BUILD_ROOT%{_bindir}/fish
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/mimedb
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/fishd
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/fish_indent
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/fish_pager

# Zip the man pages
/bin/gzip $RPM_BUILD_ROOT%{_datadir}/fish/man/man1/*

%find_lang %{name}


%post
# Add fish to the list of allowed shells in /etc/shells
if ! grep %{_bindir}/fish %{_sysconfdir}/shells >/dev/null; then
    echo %{_bindir}/fish >>%{_sysconfdir}/shells
fi


%postun
# Remove fish from the list of allowed shells in /etc/shells
if [ "$1" = 0 ]; then
    grep -v %{_bindir}/fish %{_sysconfdir}/shells >%{_sysconfdir}/fish.tmp
    mv %{_sysconfdir}/fish.tmp %{_sysconfdir}/shells
fi


%files -f %{name}.lang

%defattr(-,root,root,-)

# The documentation directory
%doc %_datadir/doc/%{name}-%{version}

# man files
%{_mandir}/man1/*.1*

# The program binaries
%attr(0755,root,root) %_bindir/*

# Configuration files
%dir %_sysconfdir/fish
%config(noreplace) %_sysconfdir/fish/config.fish

# Non-configuration initialization files
%dir %_datadir/fish
%_datadir/fish/config.fish

# Program specific tab-completions
%dir %_datadir/fish/completions
%_datadir/fish/completions/*.fish

# Dynamically loaded shellscript functions
%dir %_datadir/fish/functions
%_datadir/fish/functions/*.fish

# Documentation for builtins and shellscript functions
%dir %_datadir/fish/man
%_datadir/fish/man/man1/*.1.gz

# Tools
%dir %_datadir/fish/tools
%_datadir/fish/tools/*.py
%_datadir/fish/tools/*.pyc
%_datadir/fish/tools/*.pyo
%_datadir/fish/tools/web_config/*.py
%_datadir/fish/tools/web_config/*.pyc
%_datadir/fish/tools/web_config/*.pyo
%_datadir/fish/tools/web_config/delete.png
%_datadir/fish/tools/web_config/index.html
%_datadir/fish/tools/web_config/jquery.js
%_datadir/fish/tools/web_config/sample_prompts/*.fish


%changelog
* Sat Jun 15 2013 Laurence McGlashan<laurence.mcglashan@gmail.com> 2.0.0-1
- fish-2.0.0
