<section id="main" role="main">
    <!-- START Template Container -->
    <div class="container-fluid">
        <!-- Page Header -->
        <div class="page-header page-header-block">
            <div class="page-header-section">
                <h4 class="title semibold">Add New Engine</h4>
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
                <form class="panel panel-default form-horizontal form-bordered" action="/new_engine" method="post" data-parsley-validate>
                    <div class="panel-heading">
                        <h3 class="panel-title"><i class="ico-tshirt mr5"></i>Engine Details</h3>
                    </div>               
                    <div class="panel-body">
                    <div class="form-group">
                        <label class="col-sm-2 control-label">Engine Name</label>
                        <div class="col-sm-6">
                            <input type="text" name="engine" class="form-control" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-2 control-label">Command</label>
                        <div class="col-sm-6">
                            <input type="text" name="cmd" class="form-control" data-parsley-type="number" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-2 control-label">Run At</label>
                        <div class="col-sm-6">
                            <input type="text" name="run_at" class="form-control" id="time-picker" placeholder="Select a time" required>
                        </div>
                    </div>
                    <div class="panel-footer">
                        <button type="submit" class="btn btn-primary">Submit</button>
                        <button type="reset" class="btn btn-inverse">Reset</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>