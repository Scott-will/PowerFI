import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'player-search',
  imports: [],
  templateUrl: './player-search.component.html',
  styleUrl: './player-search.component.css'
})
export class PlayerSearchComponent {
  searchProperties = [
    { label: 'First Name', value: 'first_name' },
    { label: 'Last Name', value: 'last_name' },
    { label: 'Position', value: 'position' },
    { label: 'Team', value: 'team' },
  ];
  queryProperty : string = this.searchProperties[0].value
  queryValue = ""

  onPropertyChange(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    this.queryProperty = selectElement.value;
  }

  onInputChange(event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    this.queryValue = inputElement.value;
  }

  @Output() searchChange = new EventEmitter<{property: string, value: string}>();

  onSubmit() {
    this.searchChange.emit({
      property: this.queryProperty,
      value: this.queryValue
    });
  }
}
