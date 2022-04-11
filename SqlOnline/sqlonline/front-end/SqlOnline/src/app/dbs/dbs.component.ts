import { Component, OnInit, ViewChild, Inject } from '@angular/core';
import { MatTable } from '@angular/material/table';
import { MatIconRegistry } from "@angular/material/icon";
import { DomSanitizer } from "@angular/platform-browser";
import { DBColumn } from '../_models/DBColumn';
import { DBTable } from '../_models/DBTable';
import { DBDatabase } from '../_models/DBDatabase';
import { ApiService } from '../_services/api.service';
import { Response } from '../_models/Response';
import { DBInfo } from '../_models/DBInfo';


@Component({
  selector: 'app-dbs',
  templateUrl: './dbs.component.html',
  styleUrls: ['./dbs.component.scss']
})
export class DbsComponent implements OnInit {

  constructor(private matIconRegistry: MatIconRegistry, private domSanitizer: DomSanitizer, private api: ApiService) {
    this.matIconRegistry.addSvgIcon(
      `db_settings`,
      this.domSanitizer.bypassSecurityTrustResourceUrl(`../assets/svg/database-settings.svg`)
    );
    this.matIconRegistry.addSvgIcon(
      `db_create`,
      this.domSanitizer.bypassSecurityTrustResourceUrl(`../assets/svg/database-create.svg`)
    );
    this.matIconRegistry.addSvgIcon(
      `table`,
      this.domSanitizer.bypassSecurityTrustResourceUrl(`../assets/svg/table.svg`)
    );
  }

  @ViewChild(MatTable) _table!: MatTable<DBColumn>;

  userDbs: Array<DBInfo> = new Array;

  ngOnInit(): void {
    this.api.getUserDbs().subscribe(
      (data: Response) => {
        if (data.success) {
          this.userDbs = data?.data;
        } else {
          this.message = "No DB found";
        }
      }
    )
  }

  displayedColumns = ["columnName", "varType"];
  isTableManagerVisable = false;
  isDBManagerVisable = false;
  isDBInfoVisable = false;

  currentDBInfo: DBInfo | null = null;

  varTypes = [
    "INTEGER",
    "REAL",
    "TEXT",
    "BLOB"
  ]

  message = "";

  newTable: DBTable = {
    tableName: "",
    columns: new Array
  };

  newDatabase: DBDatabase = {
    name: "",
    description: "",
    tables: new Array
  }

  addColumn(colName:string, varType:string) {
    if (colName) {
    let column: DBColumn = {
      columnName: colName,
      varType: varType
    }
    this.newTable.columns.push(column);
    this._table.renderRows();
    }
  }

  deleteColumn() {
    this.newTable.columns.pop();
    this._table.renderRows();
  }

  addTable(tableName: string) {
    if (tableName) {
    this.newTable.tableName = tableName;
    this.newDatabase.tables.push(this.newTable);
    this.newTable = {
      tableName: "",
      columns: new Array
    };
    this._table.renderRows();
    this.closeTableManager();
    }
  }

  openTableManager() {
    this.isTableManagerVisable = true;
  }

  closeTableManager() {
    this.isTableManagerVisable = false;
  }

  openDBManager() {
    this.message = "";
    this.isDBManagerVisable = true;
    this.currentDBInfo = null;
  }

  closeDBManager() {
    this.isDBManagerVisable = false;
  }

  addDB(dbName: string, dbDescription: string) {
    if (dbName) {
      this.newDatabase.name = dbName;
      this.newDatabase.description = dbDescription;
      this.api.createNewDB(this.newDatabase).subscribe(
        (data: Response) => {
          if (data.success) {
            this.message = "Success";
            this.newDatabase = {
              name: "",
              description: "",
              tables: new Array
            }
            this.ngOnInit();
          } else {
            this.message = "Error: " + data?.data;
          }
        }
      )
      console.log(this.newDatabase);
      this.closeDBManager();
      this.closeTableManager();
    }
  }

  openDialog(dBInfo: DBInfo) {
    this.currentDBInfo = dBInfo;
  }

  
}
