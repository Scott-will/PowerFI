import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TransactiontreeComponent } from './transactiontree.component';

describe('TransactiontreeComponent', () => {
  let component: TransactiontreeComponent;
  let fixture: ComponentFixture<TransactiontreeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TransactiontreeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TransactiontreeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
