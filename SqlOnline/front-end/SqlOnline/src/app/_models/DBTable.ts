import { DBColumn } from "./DBColumn"


export interface DBTable {
    tableName: string,
    columns: Array<DBColumn>
}