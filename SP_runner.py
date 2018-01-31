import cx_Oracle
import rope_logger as tl
from env_property import (BD_HOST_IOD, DB_PORT_IOD, DB_SID_IOD, DB_USR_IOD, BD_PWD_IOD)


def run_tree_sp(db_flag, stored_proc_name, parameters):
    """Execute stored procedures in TreE DB table"""
    if db_flag == 'IOD':
        dsn_str_iod = cx_Oracle.makedsn(BD_HOST_IOD, DB_PORT_IOD, service_name=DB_SID_IOD)
        try:
            con_iod = cx_Oracle.connect(user=DB_USR_IOD, password=BD_PWD_IOD, dsn=dsn_str_iod)
            connector_1 = con_iod.cursor()
            print(' Executing Stored Proc >> ' + stored_proc_name)
            tl.test_logger.info(' Executing Stored Proc >> ' + stored_proc_name)
            if parameters != '':
                connector_1.callproc(stored_proc_name, parameters)
            else:
                connector_1.callproc(stored_proc_name)
            print(stored_proc_name + ' >> Stored Proc executed.')
            tl.test_logger.info(stored_proc_name + ' >> Stored PROC executed successfully.')
            con_iod.close()
        except SystemError as err:
            print('Failed to connect to TREE DB.')
            tl.test_logger.debug('Can not establish DB connection as: ', str(err))
# sp_name = 'pkg_tre_etls.load_report_trade_pfolio_map'
# sp_parameters = ['66333718','LANDED','TEST','4767904093_TREETH_07','INFINITY','BACKLOAD']
# run_tree_sp('IOD', sp_name, '')
