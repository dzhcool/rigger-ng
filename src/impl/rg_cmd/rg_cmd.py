#coding=utf8
import  os,re ,logging

from utls.rg_io  import rgio,export_objdoc ,rg_logger
from rg_cmd_base import rg_cmd , cmdtag_rg , cmdtag_prj ,cmdtag_pub

import res,  interface
import conf

import impl.rg_dev , impl.rg_ioc




class init_cmd(rg_cmd) :
    def _execute(self,rargs):
        dst = os.getcwd() + "/_rg"
        if os.path.exists(dst) :
            raise interface.rigger_exception("have _rg dir. maybe inited!")

        import utls.tpl
        tpl = rargs.rg.root + "/rg_tpl"
        utls.tpl.tplworker().execute(tpl,dst)

class tpl_cmd(rg_cmd) :
    def _config(self,argv,rargs):
        dst = ""
        tpl = ""
        if argv.has_key('-t') :
            tpl  = argv['-t']
        if argv.has_key('-o') :
            dst  = argv['-o']
        if len(dst) == 0 :
            print("rg tpl -t <template> -o <dst>")
            raise interface.rigger_exception("dst: %s is empty" %dst)
        if os.path.exists(dst) :
            raise interface.rigger_exception("dst: %s have exists" %dst)
        if not os.path.exists(tpl) :
            raise interface.rigger_exception("tpl: %s not exists" %tpl)
        self.dst = dst
        self.tpl = tpl
    def _execute(self,rargs):
        import utls.tpl
        utls.tpl.tplworker().execute(self.tpl,self.dst)

class help_cmd(rg_cmd,cmdtag_rg):
    @staticmethod
    def cmd_help(cmdname):
        cmdobj = impl.rg_ioc.ins_cmd(cmdname)
        cmdobj.useage(rgio.simple_out)

    @staticmethod
    def res_help(resname):
        resobj  = impl.rg_ioc.ins_res(resname)
        if resobj is None :
            raise  interface.rigger_exception( "instance res fail! resname: %s" %(resname) )
        resobj.useage(rgio.simple_out)

    def _execute(self,rargs):
        conf.version.file=os.path.join(rargs.rg.root ,"version.txt" )
        ver    = conf.version()
        rgio.simple_out("rigger-ng ver: " + ver.info())
        cmdlen = len(rargs.prj.cmds)
        print(rargs.prj.cmds)
        if cmdlen == 1 :
            rargs.help()
            impl.rg_ioc.list_cmd()
            return
        if cmdlen >= 2 :
            subcmd = rargs.prj.cmds[1]
            if subcmd == "res":
                if cmdlen == 3 :
                    resname = rargs.prj.cmds[2]
                    help_cmd.res_help(resname)
                else:
                    impl.rg_ioc.list_res()
            else:
                cmdname = rargs.prj.cmds[1]
                help_cmd.cmd_help(cmdname)





