<section id="main" role="main">
    <!-- START Template Container -->
    <div class="container-fluid">
        <!-- Page Header -->
        <div class="page-header page-header-block">
            <div class="page-header-section">
                <h4 class="title semibold">Edit Site Config</h4>
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
                <form class="panel panel-default form-horizontal form-bordered" action="/site_config/{{ engine_name }}/{{ domain.replace('.', '_') }}/edit" method="post" data-parsley-validate>
                    <div class="panel-heading">
                        <h3 class="panel-title"><i class="ico-tshirt mr5"></i>Site Config Details</h3>
                    </div>               
                    <div class="panel-body">
                    <div class="form-group">
                        <label class="col-sm-2 control-label">Channel Name</label>
                        <div class="col-sm-6">
                            <input type="text" name="channel" class="form-control" value="{{ engine_name[0].upper() + engine_name[1:] }}" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-2 control-label">Domain Name</label>
                        <div class="col-sm-6">
                            <input type="text" read-only name="engine" class="form-control" value="{{ domain }}" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-2 control-label">Configuration</label>
                        <div class="col-sm-6">
                            <textarea name="configuration" class="form-control" rows="10">{{ configuration }}</textarea>
                        </div>
                    </div>
                    <div class="panel-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="reset" class="btn btn-inverse">Reset</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>