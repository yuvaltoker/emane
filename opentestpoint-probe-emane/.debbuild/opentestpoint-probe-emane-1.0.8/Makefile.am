EXTRA_DIST= \
 AUTHORS \
 COPYING \
 MANIFEST.in \
 setup.py.in \
 autogen.sh \
 $(PACKAGE).spec.in \
 otestpoint \
 meta \
 emm-gen \
 debian

BUILT_SOURCES = \
 setup.py \
 $(PACKAGE).spec \
 otestpoint/emane/physicallayer.proto \
 otestpoint/emane/probe-emane-physicallayer.xsd \
 otestpoint/emane/physicallayer_pb2.py \
 otestpoint/emane/rfpipe.proto \
 otestpoint/emane/probe-emane-rfpipe.xsd \
 otestpoint/emane/rfpipe_pb2.py \
 otestpoint/emane/ieee80211abg.proto \
 otestpoint/emane/probe-emane-ieee80211abg.xsd \
 otestpoint/emane/ieee80211abg_pb2.py \
 otestpoint/emane/commeffect.proto \
 otestpoint/emane/probe-emane-commeffect.xsd \
 otestpoint/emane/commeffect_pb2.py \
 otestpoint/emane/virtualtransport.proto \
 otestpoint/emane/probe-emane-virtualtransport.xsd \
 otestpoint/emane/virtualtransport_pb2.py \
 otestpoint/emane/rawtransport.proto \
 otestpoint/emane/probe-emane-rawtransport.xsd \
 otestpoint/emane/rawtransport_pb2.py \
 otestpoint/emane/tdmaeventschedulerradiomodel.proto \
 otestpoint/emane/probe-emane-tdmaeventschedulerradiomodel.xsd \
 otestpoint/emane/tdmaeventschedulerradiomodel_pb2.py \
 otestpoint/emane/physicallayerreceivepowertable_pb2.py \
 otestpoint/emane/eventreceptiontable_pb2.py \
 otestpoint/emane/pathlosseventtable_pb2.py

all-local:
	$(PYTHON) setup.py build

dist-hook:
	find $(distdir) -name "*_pb2.py" -delete
	find $(distdir) -name "*.xsd" -delete
	rm -f $(distdir)/otestpoint/emane/commeffect.proto
	rm -f $(distdir)/otestpoint/emane/ieee80211abg.proto
	rm -f $(distdir)/otestpoint/emane/physicallayer.proto
	rm -f $(distdir)/otestpoint/emane/rawtransport.proto
	rm -f $(distdir)/otestpoint/emane/rfpipe.proto
	rm -f $(distdir)/otestpoint/emane/virtualtransport.proto
	rm -f $(distdir)/otestpoint/emane/tdmaeventschedulerradiomodel.proto

clean-local: setup.py cleandeb
	$(PYTHON) setup.py clean
	-rm -rf build
	-rm -rf dist
	-rm -rf deb_dist
	-rm -f $(BUILT_SOURCES)
	-find . -name "*.pyc" -delete
	-rm -rf opentestpoint_probe_emane.egg-info
	-rm -f opentestpoint-probe-emane-*.tar.gz
	-rm -f $(PACKAGE).spec
	-rm -rf .rpmbuild
	-rm -rf .debbuild
	-rm -f debian/changelog
	-rm -f .installedfiles

DISTCLEANFILES=setup.py

sdist:
	$(PYTHON) setup.py sdist

edit = sed                              \
        -e 's|@VERSION[@]|$(VERSION)|g' \
        -e 's|@PYTHON[@]|$(PYTHON)|g'   \
        -e 's|@DEBIAN_VERSION[@]|$(DEBIAN_VERSION)|g' \
        -e 's|@DATE_RFC2822[@]|$(DATE_RFC2822)|g'

setup.py:	setup.py.in
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

install-exec-hook: $(BUILT_SOURCES)
	$(PYTHON) setup.py install \
        -O1 \
        --single-version-externally-managed \
        --record .installedfiles \
        --prefix=$(prefix) \
        --exec-prefix=$(exec_prefix) \
        $(if $(DESTDIR),--root=$(DESTDIR)) \
        $(if $(subst false,,$(HAVE_DEB)),--install-layout=deb)

uninstall-hook:
	if test -f .installedfiles; then xargs -a .installedfiles rm -f; fi

RPMARCH=`arch`

if HAVE_RPMBUILD

if HAVE_PYTHON2
RPMBUILD_ARGS=--with python2
else
RPMBUILD_ARGS=
endif

rpm: $(PACKAGE).spec dist-gzip
	mkdir -p .rpmbuild/BUILD \
	.rpmbuild/SPECS \
	.rpmbuild/SOURCES \
	.rpmbuild/SRPMS \
	.rpmbuild/RPMS/noarch \
	.rpmbuild/tmp
	cp -f $(PACKAGE)-$(VERSION).tar.gz .rpmbuild/SOURCES
	rpmbuild --clean -ba $(top_srcdir)/$(PACKAGE).spec --target $(RPMARCH) \
    --define "_topdir $$PWD/.rpmbuild" \
    --define "_tmppath $$PWD/.rpmbuild/tmp" \
    $(RPMBUILD_ARGS)
	@echo "============================================================"
	@echo "RPMs located in .rpmbuild/RPMS and .rpmbuild/SRPMS"

endif

if HAVE_DEB

deb: dist-gzip
	rm -rf .debbuild
	mkdir -p .debbuild
	cp -f $(PACKAGE)-$(VERSION).tar.gz .debbuild
	cd .debbuild && tar xzf $(PACKAGE)-$(VERSION).tar.gz
	$(edit) .debbuild/$(PACKAGE)-$(VERSION)/debian/changelog.in > \
          .debbuild/$(PACKAGE)-$(VERSION)/debian/changelog
if HAVE_PYTHON2
	cp .debbuild/$(PACKAGE)-$(VERSION)/debian/control.with-python2 \
              .debbuild/$(PACKAGE)-$(VERSION)/debian/control
	cp .debbuild/$(PACKAGE)-$(VERSION)/debian/rules.with-python2 \
              .debbuild/$(PACKAGE)-$(VERSION)/debian/rules
endif
	cd .debbuild/$(PACKAGE)-$(VERSION) && dpkg-buildpackage -F -us -uc
	@echo "============================================================"
	@echo "debs located in .debbuild"
cleandeb:
	dh_clean
else

cleandeb:

endif

$(PACKAGE).spec: $(PACKAGE).spec.in
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@


otestpoint/emane/physicallayer.proto otestpoint/emane/physicallayer.xsd: meta/emanephy.xml
	$(PYTHON) ./emm-gen -o PhysicalLayer --category EMANE -p otestpoint/emane $<

otestpoint/emane/rfpipe.proto otestpoint/emane/rfpipe.xsd: meta/rfpipe.xml
	$(PYTHON) ./emm-gen -o RFPipe --category EMANE -p otestpoint/emane $<

otestpoint/emane/ieee80211abg.proto otestpoint/emane/ieee80211abg.xsd: meta/ieee80211abg.xml
	$(PYTHON) ./emm-gen -o IEEE80211abg --category EMANE -p otestpoint/emane $<

otestpoint/emane/commeffect.proto otestpoint/emane/commeffect.xsd: meta/commeffect.xml
	$(PYTHON) ./emm-gen -o CommEffect --category EMANE -p otestpoint/emane $<

otestpoint/emane/virtualtransport.proto otestpoint/emane/virtualtransport.xsd: meta/transvirtual.xml
	$(PYTHON) ./emm-gen -o VirtualTransport --category EMANE -p otestpoint/emane $<

otestpoint/emane/rawtransport.proto otestpoint/emane/rawtransport.xsd: meta/transraw.xml
	$(PYTHON) ./emm-gen -o RawTransport --category EMANE -p otestpoint/emane $<

otestpoint/emane/tdmaeventschedulerradiomodel.proto otestpoint/emane/tdmaeventschedulerradiomodel.xsd: meta/tdmaeventschedulerradiomodel.xml
	$(PYTHON) ./emm-gen -o TDMAEventSchedulerRadioModel --category EMANE -p otestpoint/emane $<

otestpoint/emane/physicallayer_pb2.py: otestpoint/emane/physicallayer.proto
	protoc -I. -I=otestpoint/emane -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/rfpipe_pb2.py: otestpoint/emane/rfpipe.proto
	protoc -I. -I=otestpoint/emane -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/ieee80211abg_pb2.py: otestpoint/emane/ieee80211abg.proto
	protoc -I. -I=otestpoint/emane -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/commeffect_pb2.py: otestpoint/emane/commeffect.proto
	protoc -I. -I=otestpoint/emane -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/virtualtransport_pb2.py: otestpoint/emane/virtualtransport.proto
	protoc -I. -I=otestpoint/emane -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/rawtransport_pb2.py: otestpoint/emane/rawtransport.proto
	protoc -I. -I=otestpoint/emane -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/tdmaeventschedulerradiomodel_pb2.py: otestpoint/emane/tdmaeventschedulerradiomodel.proto
	protoc -I. -I=otestpoint/emane -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/physicallayerreceivepowertable_pb2.py: otestpoint/emane/physicallayerreceivepowertable.proto
	protoc -I. -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/eventreceptiontable_pb2.py: otestpoint/emane/eventreceptiontable.proto
	protoc -I. -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@

otestpoint/emane/pathlosseventtable_pb2.py: otestpoint/emane/pathlosseventtable.proto
	protoc -I. -I=$(libotestpoint_PROTODIR) --python_out=. $<
	sed -i -e 's/import measurementtable_pb2/from otestpoint.interface import measurementtable_pb2/' $@
