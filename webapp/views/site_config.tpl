<section id="main" role="main">
    <!-- START Template Container -->
    <div class="container-fluid">
        <!-- Page Header -->
        <div class="page-header page-header-block">
            <div class="page-header-section">
                <h4 class="title semibold">Site Configurations</h4>
            </div>
            <div class="page-header-section">
                <!-- Toolbar -->
                <!-- <div class="toolbar">
                    <ol class="breadcrumb breadcrumb-transparent nm">
                        <li><a href="#">Table</a></li>
                        <li class="active">Default</li>
                    </ol>
                </div> -->
                <!--/ Toolbar -->
            </div>
        </div>
        <!-- Page Header -->

        <!-- START row -->
        <div class="row">
            <div class="col-md-12">
                <!-- START panel -->
                <div class="panel panel-primary">
                    <!-- panel heading/header -->
                    <div class="panel-heading">
                        <h3 class="panel-title"><span class="panel-icon mr5"><i class="ico-table22"></i></span>Site Configurations</h3>
                        <!-- panel toolbar -->
                        <div class="panel-toolbar text-right">
                            <!-- option -->
                            <div class="option">
                                <button class="btn up" data-toggle="panelcollapse"><i class="arrow"></i></button>
                                <button class="btn" data-toggle="panelremove" data-parent=".col-md-12"><i class="remove"></i></button>
                            </div>
                            <!--/ option -->
                        </div>
                        <!--/ panel toolbar -->
                    </div>
                    <!--/ panel heading/header -->
                    <!-- panel toolbar wrapper -->
                    <div class="panel-toolbar-wrapper pl0 pt5 pb5">
                        <div class="panel-toolbar text-right">
                            <button onclick="window.location.href='/site_config/{{ engine }}/add';" type="button" class="btn btn-success mb5"><i class="ico-user22"></i> Add New Site Config</button>
                        </div>
                    </div>
                    <!--/ panel toolbar wrapper -->

                    <!-- panel body with collapse capabale -->
                    <div class="table-responsive panel-collapse pull out">
                        <table class="table table-bordered table-hover" id="table1">
                            <thead>
                                <tr>
                                    <th width="15%">Site Name</th>
                                    <th>Path</th>
                                    <th width="10%"></th>
                                </tr>
                            </thead>
                            <tbody>
                                % for site_config in site_configs:
                                <tr>
                                    <td>{{ site_config }}</td>
                                    <td>{{ "%s/%s.txt" % (site_config_path, site_config) }}</td>
                                    <td class="text-center">
                                        <!-- button toolbar -->
                                        <div class="toolbar">
                                            <div class="btn-group">
                                                <button type="button" class="btn btn-sm btn-default">Action</button>
                                                <button type="button" class="btn btn-sm btn-default dropdown-toggle" data-toggle="dropdown">
                                                    <span class="caret"></span>
                                                </button>
                                                <ul class="dropdown-menu dropdown-menu-right">
                                                    <li><a href="/site_config/{{ engine }}/{{ site_config.replace('.', '_') }}/edit"><i class="icon ico-pencil"></i>Edit</a></li>
                                                    <li class="divider"></li>
                                                    <li><a href="/site_config/{{ engine }}/{{ site_config.replace('.', '_') }}/delete" class="text-danger" ><i class="icon ico-print3"></i>Delete</a></li>
                                                </ul>
                                            </div>
                                        </div>
                                        <!--/ button toolbar -->
                                    </td>
                                </tr>
                                % end
                            </tbody>
                        </table>
                    </div>
                    <!--/ panel body with collapse capabale -->
                </div>
            </div>
        </div>
        <!--/ END row -->
                        
    </div>
    <!--/ END Template Container -->

    <!-- START To Top Scroller -->
    <a href="#" class="totop animation" data-toggle="waypoints totop" data-showanim="bounceIn" data-hideanim="bounceOut" data-offset="50%"><i class="ico-angle-up"></i></a>
    <!--/ END To Top Scroller -->

</section>