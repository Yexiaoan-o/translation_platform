import dolphindb as ddb
import pandas as pd
import datetime
import logging

logger = logging.getLogger("uvicorn.error")

class DDBManager:
    def __init__(self, host="127.0.0.1", port=8848):
        self.s = ddb.session()
        self.s.connect(host, port, "admin", "123456")
        self.db_path = "dfs://TranslationPlatform"
        self._init_db()

    def _init_db(self):
        script = f"""
        if(!existsDatabase("{self.db_path}")){{
            db = database("{self.db_path}", VALUE, 2026.01M..2026.12M)
            t_proj = table(1:0, `id`name`status`created_at, [SYMBOL, SYMBOL, SYMBOL, TIMESTAMP])
            db.createPartitionedTable(t_proj, "projects", "created_at")
            t_seg = table(1:0, `project_id`seg_id`source`target, [SYMBOL, INT, STRING, STRING])
            db.createTable(t_seg, "segments")
        }}
        """
        self.s.run(script)

    def save_project(self, project_id, name, segments):
        # 存项目信息
        df_p = pd.DataFrame({'id':[project_id], 'name':[name], 'status':['active'], 'created_at':[datetime.datetime.now()]})
        self.s.upload({"new_p": df_p})
        self.s.run(f"loadTable('{self.db_path}', 'projects').append!(new_p)")
        # 存句段信息
        df_s = pd.DataFrame({
            'project_id': [project_id]*len(segments),
            'seg_id': [s['id'] for s in segments],
            'source': [s['source'] for s in segments],
            'target': [s.get('target', '') for s in segments]
        })
        self.s.upload({"new_s": df_s})
        self.s.run(f"loadTable('{self.db_path}', 'segments').append!(new_s)")

    def get_all_projects(self):
        return self.s.run(f"select * from loadTable('{self.db_path}', 'projects') order by created_at desc").to_dict(orient='records')

    def load_segments(self, pid):
        return self.s.run(f"select seg_id as id, source, target from loadTable('{self.db_path}', 'segments') where project_id='{pid}' order by seg_id").to_dict(orient='records')

    def update_segment_translation(self, pid, seg_id, target):
        script = f"update loadTable('{self.db_path}', 'segments') set target='{target}' where project_id='{pid}' and seg_id={seg_id}"
        self.s.run(script)

    def delete_project(self, project_id: str):
        # 1. 删除句段表中的数据
        script_seg = f"delete from loadTable('{self.db_path}', 'segments') where project_id='{project_id}'"
        self.s.run(script_seg)
        
        # 2. 删除项目信息表中的数据
        script_proj = f"delete from loadTable('{self.db_path}', 'projects') where id='{project_id}'"
        self.s.run(script_proj)
        logger.info(f"项目 {project_id} 已从 DolphinDB 中彻底删除")