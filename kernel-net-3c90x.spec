
# conditional build
# _without_dist_kernel          without distribution kernel

%define		_orig_name	3c90x
%define		_rel		3

Summary:	Linux driver for the 3Com 3C90x and 3C980 Network Interface Cards
Summary(pl):	Sterownik dla Linuksa do kart sieciowych 3Com 3C90x i 3C980
Name:		kernel-net-%{_orig_name}
Version:	1.0.2
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://support.3com.com/infodeli/tools/nic/linux/%{_orig_name}-%(echo %{version} | sed -e 's/\.//g').tar.gz
URL:		http://support.3com.com/infodeli/tools/nic/linux.htm
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is 3Com's EtherLink PCI driver for Linux. It provides support for
the 3c90x and 3c980 network adapters.

%description -l pl
Sterownik dla Linuksa do kart sieciowych 3Com 3c90x i 3c980.

%package -n kernel-smp-net-%{_orig_name}
Summary:	Linux SMP driver for the 3Com 3C90x i 3C980 Network Interface Cards
Summary(pl):	Sterownik dla Linuksa SMP do kart sieciowych 3Com 3C90x i 3C980
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-net-%{_orig_name}
This is 3Com's EtherLink PCI driver for Linux SMP. It provides support
for the 3c90x and 3c980 network adapters.

%description -n kernel-smp-net-%{_orig_name} -l pl
Sterownik dla Linuksa SMP do kart sieciowych 3Com 3c90x i 3c980.

%prep
%setup -q -n %{_orig_name}-%(echo %{version} | sed -e 's#\.##g')

%build
rm -f %{_orig_name}.o
%{kgcc} -o %{_orig_name}.o -c %{rpmcflags}  -c -DMODULE -D__KERNEL__ -O2 -DSMP=1 -D__SMP__ -DCONFIG_X86_LOCAL_APIC -Wall -Wstrict-prototypes -I%{_kernelsrcdir}/include %{_orig_name}.c
mv -f %{_orig_name}.o %{_orig_name}-smp.o
%{kgcc} -o %{_orig_name}.o -c %{rpmcflags}  -c -DMODULE -D__KERNEL__ -O2 -Wall -Wstrict-prototypes -I%{_kernelsrcdir}/include %{_orig_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install %{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
install %{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

gzip -9nf readme

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc *.gz 
/lib/modules/%{_kernel_ver}smp/misc/*
