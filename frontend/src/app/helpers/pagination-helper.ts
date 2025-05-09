export class PaginationHelper{
    totalItems = 0;
    pageSize = 10;
    pageIndex = 1;
    pageSizeOptions = [5, 10, 20, 50];
    loaderCallback: () => void;

  constructor(callback: () => void) {
    this.loaderCallback = callback;
  }
    get totalPages() {
       return Math.ceil(this.totalItems / this.pageSize);
    }
  
    goToPage(page: number) {
    if (page >= 1 && page <= this.totalPages) {
        this.pageIndex = page;
        this.loaderCallback();
    }
    }
    nextPage() {
      this.goToPage(this.pageIndex + 1);
    }

    prevPage() {
    this.goToPage(this.pageIndex - 1);
    this.loaderCallback();
    }
}