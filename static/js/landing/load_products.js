const loadProducts = (page, url, detail_url) => {
    let current_page = Number(page);

    $.ajax({
        url: url,
        type: "GET",
        data: {
            page: page,
            search: $("#search").val(),
        },
        dataType: "json",
        success: function (response) {
            $("#load-more-products").show();

            if (response.products.length > 0) {
                $.each(response.products, function (index, product) {
                    const product_detail_url = detail_url.replace("0", product.id);

                    $("#products_div").append(`
                        <div class="col-md-4 col-sm-6 col-xs-12 margin_bottom_30_all">
                            <div class="product_list">
                                <div class="product_img">
                                    <img class="img-responsive" src="${product.image}" alt="" />
                                </div>
                                <div class="product_detail_btm">
                                    <div class="center">
                                        <h4>
                                            <a href="${product_detail_url}">${product.name}</a>
                                        </h4>
                                    </div>
                                    <div class="starratin">
                                        <div class="center">
                                            <i class="fa fa-star" aria-hidden="true"></i>
                                            <i class="fa fa-star" aria-hidden="true"></i>
                                            <i class="fa fa-star" aria-hidden="true"></i>
                                            <i class="fa fa-star" aria-hidden="true"></i>
                                            <i class="fa fa-star" aria-hidden="true"></i>
                                        </div>
                                    </div>
                                    <div class="product_price">
                                        <p>
                                            <span class="new_price">$ ${product.price}</span>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `);
                });
            }

            if (response.products.length < 1 && current_page === 1) {
                $("#load-more-products").hide();
                $("#products_div").append(`
                    <div class="col-md-12">
                        <div class="alert alert-warning text-center" role="alert">
                            No hay porductos para mostrar
                        </div>
                    </div>
                `);
            }

            if (response.has_next) {
                current_page += 1;
                $("#load-more-products").attr("data-page", current_page);
            } else {
                $("#load-more-products").hide();
            }
        },
    });
};
