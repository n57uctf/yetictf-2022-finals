import { DBTable } from "./DBTable";

export interface DBDatabase {
    name: string,
    description: string,
    tables: Array<DBTable>
}